use std::{ collections::HashMap, env::{ args, current_dir }, error::Error, fs, path::PathBuf };

fn main() /*-> Result<(), Box<dyn Error>>*/ {
    let args: Vec<String> = args().collect();

    let src = get_abs(&args[1]).unwrap();
    let dest = get_abs(&args[2]).unwrap();

    let file_map = read_dir(&src, &dest).unwrap();

    file_map.iter().for_each(|entry| {
        println!("{:?} -> {:?}", *entry.0, *entry.1);
    });

    // Ok(())
}

fn get_abs(path: &String) -> Result<PathBuf, Box<dyn Error>> {
    let p = PathBuf::from(path);

    let abs_path = if !p.is_absolute() {
        let mut cur_dir = current_dir()?;
        cur_dir.push(p);
        cur_dir=PathBuf::from(cur_dir.canonicalize()?);
        println!("{:?}", cur_dir);
        cur_dir
    } else {
        p
    };

    Ok(abs_path)
}

fn read_dir(
    src_root: &PathBuf,
    dest_root: &PathBuf
) -> Result<HashMap<PathBuf, PathBuf>, Box<dyn Error>> {
    let mut file_map: HashMap<PathBuf, PathBuf> = HashMap::new();

    match fs::read_dir(src_root) {
        Err(e) => eprintln!("Could not find directory: {}", e),
        Ok(entries) => {
            for entry in entries {
                let src_child = entry?.path();
                let leaf_name = src_child.file_name().unwrap().to_str().unwrap().to_string();

                if src_child.is_dir() {
                    let mut dest_child = dest_root.clone();
                    dest_child.push(leaf_name);
                    let child_file_map = read_dir(&src_child, &dest_child)?;
                    child_file_map.iter().for_each(|child| {
                        file_map.insert(
                            child.0.canonicalize().unwrap(),
                            child.1.canonicalize().unwrap()
                        );
                    });
                } else {
                    file_map.insert(
                        src_root.join(&leaf_name).canonicalize()?,
                        dest_root.join(&leaf_name).canonicalize()?
                    );
                }
            }
        }
    }
    Ok(file_map)
}

// fn copy(source: PathBuf, targer: PathBuf, bytes: Vec<u8>) {}
