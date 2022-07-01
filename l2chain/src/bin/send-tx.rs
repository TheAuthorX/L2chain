use serde::{Deserialize, Serialize};
use std::{
    fs::File,
    io::{self, prelude::*},
    path::PathBuf,
    sync::Mutex,
};
use structopt::StructOpt;
use core::basic::{error::anyhow::{anyhow, Result, Context, bail}};
use once_cell::sync::{Lazy, OnceCell};
use regex::Regex;

static YCSB: OnceCell<Mutex<io::BufReader<File>>> = OnceCell::new();
static YCSB_READ_RE: Lazy<Regex> =
    Lazy::new(|| Regex::new(r"^READ usertable (\w+) \[.+\]$").unwrap());
static YCSB_WRITE_RE: Lazy<Regex> =
    Lazy::new(|| Regex::new(r"^UPDATE usertable (\w+) \[ field\d+=(.+) \]$").unwrap());

#[derive(Debug, StructOpt, Serialize, Deserialize)]
#[structopt(name = "send-tx", version = "0.1")]
struct Opts {
    /// Endpoint to http tx server.
    #[structopt(long, default_value = "127.0.0.1:8000")]
    endpoint: String,

    /// Total number of DApps.
    #[structopt(long, default_value = "1")]
    dapps: u64,

    /// Total number of TX.
    #[structopt(short, long)]
    txns: usize,

    /// Number of TX per seconds.
    #[structopt(short, long)]
    rate: usize,

    /// Wait period in seconds to check block committing after sending TX.
    #[structopt(short, long, default_value = "60")]
    wait: u64,

    /// Seed used for RNG.
    #[structopt(long)]
    seed: Option<u64>,

    /// Maximum number of accounts.
    #[structopt(short, long)]
    accounts: Option<usize>,

    // List of contracts. Accepted values: kvstore.
    // #[structopt(parse(try_from_str = parse_contract_arg), required = true)]
    // contract: Vec<ContractArg>,

    // Consensus protocol. Accepted values: pow, raft
    // #[structopt(long)]
    // consensus: ConsensusProtocol,

    // TODO: modify to support all workload.txt like files
    #[structopt(
        short,
        long,
        parse(from_os_str),
        help = "Path to ycsb.txt. Used for kvstore smart contract."
    )]
    ycsb: Option<PathBuf>,
}

#[tokio::main]
async fn main() -> Result<()> {
    let opts = Opts::from_args();
    dbg!("Input opts:", &opts);

    // set ycsb file buffer. TODO: modify to support all workload.txt files
    if let Some(ycsb) = opts.ycsb.as_ref() {
        YCSB.set(Mutex::new(io::BufReader::new(File::open(ycsb)?)))
            .map_err(|_e| anyhow!("Failed to set YCSB file buffer."))?;
    }

    if opts.raft {
        let mut i = 0;
        loop {
            match get_leader(&opts.endpoint).await {
                Ok(leader) => {
                    info!("Raft Leader: {}", leader);
                    break;
                }
                Err(_) => {
                    sleep(ONE_SECOND).await;
                    i += 1;
                    if i % 60 == 0 {
                        info!("Waiting for leader election...");
                    }
                }
            }
        }
    }

    send_record_event_with_data(&opts.endpoint, "send-tx-opts", &opts).await?;

    let mut rng = match opts.seed {
        Some(seed) => StdRng::seed_from_u64(seed),
        None => StdRng::from_entropy(),
    };

    let mut contracts: Vec<(Address, ShardId, ContractArg)> =
        Vec::with_capacity(opts.contract.len());

    let deploy_txs: Vec<(SignedTxRequest, ShardId)> = opts
        .contract
        .iter()                     
        .enumerate()                
        .map(|(id, &contract)| {  
            let id = (id as u64) % opts.shard;
            let shard_id = ShardId::new(id as u64, opts.shard);  
            let (address, deploy_tx) = create_deploy_tx(&mut rng, contract, shard_id);
            debug!("tx {} address {}", id, address);
            contracts.push((address, shard_id, contract));
            (deploy_tx, shard_id)
        })
        .collect();

    info!("Deploy txs");

    let tx_count = get_tx_count(&opts.endpoint).await?;
    send_tx_requests_with_shard(&opts.endpoint, deploy_txs.into_iter()).await?;

    loop {
        sleep(Duration::from_millis(500)).await;
        let tx_count2 = get_tx_count(&opts.endpoint).await?;

        if tx_count2 >= tx_count + opts.contract.len() {
            break;
        }
    }
    info!("Deploy finished");

    if opts.raft {
        info!("Current Raft Leader: {}", get_leader(&opts.endpoint).await?);
    }

    let mut accounts: VecDeque<(Keypair, Nonce)> = {
        std::iter::repeat_with(|| (Keypair::generate(&mut rng), Nonce::zero()))
            .take(opts.accounts.unwrap_or(opts.total))
            .collect()
    };

    send_record_event(&opts.endpoint, "start-send-tx").await?;

    let begin = Instant::now();
    const ONE_SECOND: Duration = Duration::from_secs(1);
    let mut next_epoch = begin + ONE_SECOND;

    let mut reqs = Vec::with_capacity(opts.rate + 1);
    let mut next_epoch_fut = sleep_until(next_epoch);
    
    for i in 0..opts.total {
        let (address, shard_id, contract) = contracts
            .choose(&mut rng)
            .copied()
            .expect("Failed to get contract.");
        let (key, nonce) = accounts.pop_front().context("Failed to get account.")?;
   
        let tx_req = TxRequest::Call {
            nonce,
            address,
            data: contract.gen_tx_input(&mut rng)?, 
        };
        let signed_tx_req = tx_req.sign(&key);

        accounts.push_back((key, (U256::from(nonce) + 1).into()));

        reqs.push((signed_tx_req, shard_id));

        if reqs.len() == opts.rate {
            send_tx_requests_with_shard(&opts.endpoint, reqs.drain(..)).await?;
            next_epoch_fut.await;

            next_epoch += ONE_SECOND;
            next_epoch_fut = sleep_until(next_epoch);
        }

        if (i + 1) % 1_000 == 0 {
            info!("Sent #{} txs", i + 1);
        }
    }

    if !reqs.is_empty() {
        send_tx_requests_with_shard(&opts.endpoint, reqs.drain(..)).await?;
    }

    let total_time = Instant::now() - begin;
    let real_rate = (opts.total as f64) / total_time.as_secs_f64();
    send_record_event_with_data(
        &opts.endpoint,
        "end-send-tx",
        serde_json::json! {{
            "total_time_in_us": total_time.as_micros() as u64,
            "real_rate": real_rate,
        }},
    )
    .await?;

    info!("Time: {:?}", total_time);
    info!("Real rate: {:?} tx/s", real_rate);

    let mut cur_block_height = get_block_height(&opts.endpoint).await?;
    let mut block_update_time = Instant::now();

    loop {
        sleep(Duration::from_millis(500)).await;
        let height = get_block_height(&opts.endpoint).await?;

        if height > cur_block_height {
            block_update_time = Instant::now();
            cur_block_height = height;
            continue;
        } else if Instant::now() - block_update_time > Duration::from_secs(opts.wait) {
            break;
        }
    }

    info!("You can stop the nodes now by: kill -INT <pid>");

    if opts.raft {
        info!("Current Raft Leader: {}", get_leader(&opts.endpoint).await?);
    }

    send_record_event(&opts.endpoint, "quit-send-tx").await?;

    Ok(())
}
