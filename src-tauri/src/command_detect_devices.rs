use std::time::Duration;
use tokio::net::TcpStream;

use std::sync::Arc;
use tokio::sync::Semaphore;

#[tauri::command]
pub async fn fetch_devices(addresses: Vec<String>) -> Vec<String> {
    // First, check if the device is online by trying to connect to port 9012
    let semaphore = if cfg!(target_os = "macos") {
        Arc::new(Semaphore::new(256 * 8))
    } else {
        Arc::new(Semaphore::new(256 * 256))
    };

    let mut port_check_tasks = Vec::new();

    for address in addresses {
        let permit = semaphore.clone().acquire_owned().await.unwrap();

        port_check_tasks.push(tokio::spawn(async move {
            let _permit = permit;
            let is_online = check_port(&address, 9012).await;
            (address, is_online)
        }));
    }

    // collect online addresses
    let mut online_addresses = Vec::new();
    for task in port_check_tasks {
        if let Ok((address, true)) = task.await {
            online_addresses.push(address);
        }
    }

    online_addresses
}

async fn check_port(ip: &str, port: u16) -> bool {
    match tokio::time::timeout(
        Duration::from_millis(2000),
        TcpStream::connect(format!("{}:{}", ip, port)),
    )
    .await
    {
        Ok(Ok(_)) => true,
        Ok(Err(_)) => false,
        Err(_) => false,
    }
}
