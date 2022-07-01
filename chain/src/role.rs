use serde::{de::Error as SerdeError, Deserialize, Deserializer};
use std::fmt;
use core::basic::{
    DAppId,
    error::anyhow::{Context as _, Result, bail},
};


#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
pub enum Role {
    Client(DAppId),
    Executor(DAppId),
    Validator,
}

impl Default for Role {
    fn default() -> Self {
        Role::Client(DAppId::default())
    }
}

impl<'de> Deserialize<'de> for Role {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        #[derive(Copy, Clone, Deserialize)]
        #[serde(rename_all = "lowercase")]
        enum RoleType {
            Client,
            Executor,
            Validator,
        }

        impl Default for RoleType {
            fn default() -> Self {
                RoleType::Client
            }
        }

        #[derive(Deserialize)]
        struct RoleData {
            #[serde(default)]
            role: RoleType,
            #[serde(default)]
            dapp_id: Option<u64>,
            #[serde(default)]
            dapp_total: Option<u64>,
        }

        let data = RoleData::deserialize(deserializer)?;
        match data.role {
            RoleType::Client => match (data.dapp_id, data.dapp_total) {
                (Some(id), Some(total)) => Ok(Self::Client(DAppId::new(id, total))),
                (None, None) => Ok(Self::Client(DAppId::default())),
                (Some(_), None) => Err(SerdeError::missing_field("dapp_total")),
                (None, Some(_)) => Err(SerdeError::missing_field("dapp_id")),
            }
            RoleType::Executor => match (data.dapp_id, data.dapp_total) {
                (Some(id), Some(total)) => Ok(Self::Executor(DAppId::new(id, total))),
                (None, None) => Ok(Self::Executor(DAppId::default())),
                (Some(_), None) => Err(SerdeError::missing_field("dapp_total")),
                (None, Some(_)) => Err(SerdeError::missing_field("dapp_id")),
            }
            RoleType::Validator => {
                if data.dapp_id.is_some() {
                    return Err(SerdeError::custom(
                        "Field dapp_id is invalid for validator.",
                    ));
                }
                if data.dapp_total.is_some() {
                    return Err(SerdeError::custom(
                        "Field dapp_total is invalid for validator.",
                    ));
                }
                Ok(Self::Validator)
            },
        }
    }
}

impl fmt::Display for Role {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Client(DAppId { id, total }) => write!(f, "Client-{}-{}", id, total),
            Self::Executor(DAppId { id, total }) => write!(f, "Executor-{}-{}", id, total),
            Self::Validator => write!(f, "Validator"),
        }
    }
}

impl Role {
    pub fn to_user_agent(self) -> String {
        format!("{}", self)
    }

    pub fn from_user_agent(input: &str) -> Result<Self> {
        match input {
            "Validator" => return Ok(Self::Validator),
            _ => {}
        }

        let mut rest_case = input.splitn(3, '-');
        let rest_role = rest_case.next().context("Unknown User Agent.")?;
        let id = rest_case.next().context("Unknown User Agent.")?.parse()?;
        let total = rest_case.next().context("Unknown User Agent.")?.parse()?;

        match rest_role {
            "Client" => return Ok(Self::Client(DAppId::new(id, total))),
            "Executor" => return Ok(Self::Executor(DAppId::new(id, total))),
            _ => bail!("Role can only be client, executor or validator.")
        }
    }
}
