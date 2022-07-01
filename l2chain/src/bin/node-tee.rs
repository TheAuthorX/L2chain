use core::error::Result;
use core::tx_engine::TxEngine;
use common_utils::config::Config;
use std::path::PathBuf;

use tee_sig::TEESignedTx as Tx;

#[cfg(target_os = "linux")]
fn create_tx_engine(cfg: &Config, enclave: &Option<PathBuf>) -> Result<TxEngine<Tx>> {
    use tx_engine_tee::{TEEConfig, TEETxEngineWorkerFactory};
    use common_utils::tx_engine_threads;

    let tee_cfg: TEEConfig = cfg.get("tee")?;
    let factory = match enclave {
        Some(enclave) => TEETxEngineWorkerFactory::new(tee_cfg, enclave)?,
        None => TEETxEngineWorkerFactory::use_enclave_in_the_same_dir(tee_cfg)?,
    };
    Ok(TxEngine::new(tx_engine_threads(), || factory.worker()))
}

#[cfg(not(target_os = "linux"))]
fn create_tx_engine(_cfg: &Config, _enclave: &Option<PathBuf>) -> Result<TxEngine<Tx>> {
    use core::error::bail;

    bail!("not support!");
}

fn main() -> Result<()> {
    use tokio::runtime::Builder;
    Builder::new_multi_thread()
        .enable_all()
        .thread_stack_size(16 * 1024 * 1024) // increase thread stack size
        .build()
        .unwrap()
        .block_on(async { l2chain::node::node_main(create_tx_engine).await })
}
