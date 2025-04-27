use std::{ collections::HashMap, env::{ args, current_dir }, error::Error, fs, path::PathBuf };

fn main() {
    /*-> Result<(), Box<dyn Error>>*/ let args: Vec<String> = args().collect();

    let src = get_abs(&args[1]).unwrap();
    let dest = get_abs(&args[2]).unwrap();

    let file_map = read_dir(&src, &dest.to_string_lossy().to_string()).unwrap();

    file_map.iter().for_each(|entry| {
        println!("{:?} -> {}", *entry.0, *entry.1);
    });

    // Ok(())
}

fn get_abs(path: &String) -> Result<PathBuf, Box<dyn Error>> {
    let p = PathBuf::from(path);

    let abs_path = if !p.is_absolute() {
        let mut cur_dir = current_dir()?;
        cur_dir.push(p);
        cur_dir = PathBuf::from(cur_dir.canonicalize()?);
        println!("{:?}", cur_dir);
        cur_dir
    } else {
        p
    };

    Ok(abs_path)
}

fn read_dir(
    src_root: &PathBuf,
    dest_root: &String
) -> Result<HashMap<PathBuf, String>, Box<dyn Error>> {
    let mut file_map: HashMap<PathBuf, String> = HashMap::new();

    match fs::read_dir(src_root) {
        Err(e) => eprintln!("Could not find directory: {}", e),
        Ok(entries) => {
            for entry in entries {
                let src_child = entry?.path();
                let leaf_name = src_child.file_name().unwrap().to_str().unwrap();
                let mut dest_child = dest_root.clone();
                dest_child.push_str(leaf_name);

                if src_child.is_dir() {
                    let child_file_map = read_dir(&src_child, &dest_child)?;
                    child_file_map.iter().for_each(|child| {
                        file_map.insert(child.0.canonicalize().unwrap(), String::from(child.1));
                    });
                } else {
                    file_map.insert(src_root.join(&leaf_name).canonicalize()?, dest_child);
                }
            }
        }
    }
    Ok(file_map)
}

// fn copy(source: PathBuf, targer: PathBuf, bytes: Vec<u8>) {}
