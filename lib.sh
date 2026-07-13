# ~/bin/lib.sh
get_script_dir() {
  local script_path="${BASH_SOURCE[1]}"
  # Resolve symlinks
  while [ -h "$script_path" ]; do
    local dir="$(cd -P "$(dirname "$script_path")" && pwd)"
    script_path="$(readlink "$script_path")"
    [[ $script_path != /* ]] && script_path="$dir/$script_path"
  done
  echo "$(cd -P "$(dirname "$script_path")" && pwd)"
}
