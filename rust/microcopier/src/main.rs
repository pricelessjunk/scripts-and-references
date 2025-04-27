use std::{
    collections::HashMap,
    env::{ args, current_dir },
    error::Error,
    fs,
    path::PathBuf,
    rc::Rc,
};

fn main() {
    /*-> Result<(), Box<dyn Error>>*/ let args: Vec<String> = args().collect();

    let src = get_abs(&args[1]).unwrap();
    let dest = get_abs(&args[2]).unwrap();
    let dest_components: Vec<String> = dest
        .components()
        .map(|item| item.as_os_str().to_string_lossy().into_owned())
        .collect();
    let dest_rc = Rc::new(dest_components);

    let file_map = read_dir(&src, dest_rc.clone()).unwrap();

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
        cur_dir = PathBuf::from(cur_dir.canonicalize().unwrap());
        cur_dir
    } else {
        p
    };

    Ok(abs_path)
}

fn read_dir(
    src_root: &PathBuf,
    dest_root: Rc<Vec<String>>
) -> Result<HashMap<PathBuf, Rc<Vec<String>>>, Box<dyn Error>> {
    let mut file_map: HashMap<PathBuf, Rc<Vec<String>>> = HashMap::new();

    match fs::read_dir(src_root) {
        Err(e) => eprintln!("Could not find directory: {}", e),
        Ok(entries) => {
            for entry in entries {
                let src_child = entry.unwrap().path();
                let leaf_name = src_child.file_name().unwrap().to_str().unwrap().to_string();
                let dest_child = dest_root;
                dest_child.push(leaf_name);

                if src_child.is_dir() {
                    let child_file_map = read_dir(&src_child, dest_child).unwrap();
                    child_file_map.iter().for_each(|child| {
                        file_map.insert(child.0.canonicalize().unwrap(), *child.1);
                    });
                } else {
                    println!("{:?}", file_map);
                    file_map.insert(src_root.join(&leaf_name).canonicalize().unwrap(), dest_child);
                }
            }
        }
    }
    Ok(file_map)
}

// fn copy(source: PathBuf, targer: PathBuf, bytes: Vec<u8>) {}
