-- luarocks install luafilesystem

local lfs = require("lfs")

-- Table to store files by their name
local file_map = {}

-- Recursive function to walk through directories
local function walk_dir(path)
    for file in lfs.dir(path) do
        if file ~= "." and file ~= ".." then
            local full_path = path .. "/" .. file
            local attr = lfs.attributes(full_path)
            if attr.mode == "directory" then
                walk_dir(full_path)
            elseif attr.mode == "file" then
                -- Add file path to map using filename as the key
                file_map[file] = file_map[file] or {}
                table.insert(file_map[file], full_path)
            end
        end
    end
end

-- Function to print duplicates
local function print_duplicates()
    for name, paths in pairs(file_map) do
        if #paths > 1 then
            print("Duplicate file name: " .. name)
            for _, path in ipairs(paths) do
                print("  " .. path)
            end
        end
    end
end

-- Main
local start_path = arg[1] or "."  -- Default to current directory if no arg
walk_dir(start_path)
print_duplicates()
