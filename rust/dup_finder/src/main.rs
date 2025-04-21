use std::{ collections::HashMap, fs::{self}, io::stdin, path::PathBuf };


fn main() {
    let args: Vec<String> = std::env::args().collect();

    let path = if args.len() > 1 { PathBuf::from(&args[1]) } else { PathBuf::from(".") };

    let abs_path = if !path.is_absolute() {
        let mut cur_dir = std::env::current_dir().unwrap();
        cur_dir.push(path);
        cur_dir.canonicalize().unwrap()
    } else {
        path
    };

    println!("Parsing path: {}", abs_path.to_string_lossy());

    let dup_list = read_dir(&abs_path);
    println!("Duplicates found: {}", dup_list.len());

    println!("Enter prefix: ");
    let prefix = &mut String::new();
    stdin().read_line(prefix).expect("Could not read from console.");

    dup_list
        .iter()
        .filter(|e| e.1.len() > 1)
        .for_each(|entry| {
            println!("{} -> {:?}", (*entry.0), (*entry.1));
            entry.1.iter().for_each(|p| {
                /*
                Apparently can be simplified with 

                if p.to_str().map_or(false, |s| s.contains(prefix.trim_end())) {
                    println!("Deleting {:?}", p);
                    if let Err(e) = fs::remove_file(p) {
                        eprintln!("Failed to delete {:?}, Error: {}", p, e);
                    }
                }
                 */ 
                if let Some(s) = p.to_str() {
                    if s.contains(prefix.trim_end()) {
                        println!("Deleting {:?}", p);
                        if let Err(e) = fs::remove_file(p) {
                            eprintln!("Failed to delete {:?}, Error: {}", p, e);
                        }
                    }
                }
            });
        });
}

fn read_dir(path: &PathBuf) -> HashMap<String, Vec<PathBuf>> {
    let mut file_count: HashMap<String, Vec<PathBuf>> = HashMap::new();

    match fs::read_dir(path) {
        Err(e) => eprintln!("Could not find directory: {}", e),
        Ok(entries) => {
            for entry in entries {
                let child_path = entry.unwrap().path();

                if child_path.is_dir() {
                    let child_file_count = read_dir(&child_path);
                    child_file_count.iter().for_each(|child| {
                        let path_list = file_count.entry(child.0.to_string()).or_insert(Vec::new());
                        child.1.iter().for_each(|p| {
                            path_list.push(p.clone());
                        });
                    });
                } else {
                    let file_name = child_path.file_name().unwrap().to_str().unwrap().to_string();
                    file_count
                        .entry(file_name)
                        .or_insert_with(Vec::new)
                        .push(child_path);
                }
            }
        }
    }

    file_count
}
