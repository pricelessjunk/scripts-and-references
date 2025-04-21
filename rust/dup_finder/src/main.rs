use std::{collections::HashMap, fs, path::PathBuf};

fn main() {
    let args: Vec<String> = std::env::args().collect();

    let path = if args.len() > 1 {
        PathBuf::from(&args[1])
    } else {
        PathBuf::from(".")
    };

    let abs_path = if !path.is_absolute() {
        let mut cur_dir = std::env::current_dir().unwrap();
        std::env::current_dir().unwrap().push(path);
        cur_dir
    } else {
        path
    };

    println!("{}", abs_path.to_string_lossy());
    let dup_list = read_dir(&abs_path);

    dup_list.iter().filter(|e| *e.1 > 1).for_each(|entry| {
        println!("{}", (*entry.0).to_string_lossy());
    });
}

fn read_dir(path: &PathBuf) -> HashMap<PathBuf, u8> {
    let mut file_count: HashMap<PathBuf, u8> = HashMap::new();

    match fs::read_dir(path) {
        Err(e) => eprintln!("Could not find directory: {}", e),
        Ok(entries) => {
            for entry in entries {
                let child_path = entry.unwrap().path();

                if child_path.is_dir() {
                    let child_file_count = read_dir(&child_path);
                    file_count.extend(
                        child_file_count
                            .iter()
                            .map(|entry| ((*entry.0).clone(), *entry.1)),
                    );
                } else {
                    let file_name = child_path; // child_path.file_name().unwrap().to_str().unwrap().to_string();
                    let mut cur_count = *file_count.get(&file_name).unwrap_or(&0u8);
                    cur_count += 1;
                    file_count.insert(file_name, cur_count);
                }
            }
        }
    }

    file_count
}
