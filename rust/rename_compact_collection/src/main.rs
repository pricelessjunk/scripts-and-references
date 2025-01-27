use std::{env, ffi::{OsStr, OsString}, fs, path::PathBuf};

fn main() {
    let args: Vec<String> = env::args().collect();
    // dbg!(&args);

    let mut folder_path = ".";
    if args.len() > 1 {
        folder_path = &args[1];
    }

    parse_path(PathBuf::from(folder_path));
}

fn parse_path(path :PathBuf) { 
    let file_list = get_file_names_list(path);
    for file_name in file_list {
        println!("{}", file_name.to_string_lossy());
    }
}

fn get_file_names_list(dir_path: PathBuf) -> Vec<OsString> {
    let mut result: Vec<OsString> = Vec::new();
    println!("Parsing {}", dir_path.display());
    match fs::read_dir(dir_path) {
        Ok(entries) => {
            for entry in entries  {
                match entry {
                    Ok(entry) => {
                        let path = entry.path();
                        if path.is_file() {
                            if let Some(file_name) = path.file_name() {
                                // println!("{}", file_name.to_string_lossy());
                                result.push(file_name.to_os_string());
                            } 
                        }
                    }
                    Err(e) => eprintln!("Something went wrong with the iterator. {}", e)
                }
            }
        }
        Err(e) => eprintln!("Could not find directory: {}", e),
    }
    return result
}

fn extract_name(path :PathBuf) -> String { 
    return String::from("Empty");
}

fn rename_file(old_path :String, new_path :String){
    match fs::rename(old_path, new_path) {
        Ok(_) => println!("File renamed successfully."),
        Err(e) => eprintln!("Error renaming file: {}", e),
    }
}