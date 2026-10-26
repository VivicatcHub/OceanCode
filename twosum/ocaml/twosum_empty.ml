(* Two Sum : trouver deux indices i < j tels que nums.(i) + nums.(j) = target. *)

let usage = "usage: twosum <target>   (nombres lus sur stdin)"
let limit = 1_000_000_000_000_000_000

(* Renvoie Some (i, j) avec i < j et nums.(i) + nums.(j) = target, ou None.
   S'il y a plusieurs solutions : le plus petit j, puis le plus petit i.
   Doit être en O(n). *)
let two_sum (_nums : int array) (_target : int) : (int * int) option =
  (* TODO *)
  failwith "TODO: two_sum"

let die msg =
  Printf.eprintf "error: %s\n%s\n" msg usage;
  exit 1

let parse_int s =
  let n = String.length s in
  let start = if n > 0 && s.[0] = '-' then 1 else 0 in
  if start = n then die (Printf.sprintf "invalid number '%s'" s);
  for k = start to n - 1 do
    if s.[k] < '0' || s.[k] > '9' then
      die (Printf.sprintf "invalid number '%s'" s)
  done;
  (* Au-delà de 19 chiffres significatifs on est forcément hors bornes. *)
  let digits = String.sub s start (n - start) in
  let i = ref 0 in
  while !i < String.length digits - 1 && digits.[!i] = '0' do incr i done;
  if String.length digits - !i > 19 then
    die (Printf.sprintf "number out of range '%s'" s);
  match int_of_string_opt s with
  | Some v when abs v <= limit -> v
  | _ -> die (Printf.sprintf "number out of range '%s'" s)

let read_numbers () =
  let input = In_channel.input_all stdin in
  let is_blank c = c = ' ' || c = '\t' || c = '\n' || c = '\r' || c = '\012' in
  let nums = ref [] in
  let len = String.length input in
  let i = ref 0 in
  while !i < len do
    while !i < len && is_blank input.[!i] do incr i done;
    let start = !i in
    while !i < len && not (is_blank input.[!i]) do incr i done;
    if !i > start then
      nums := parse_int (String.sub input start (!i - start)) :: !nums
  done;
  Array.of_list (List.rev !nums)

let () =
  if Array.length Sys.argv <> 2 then die "wrong number of arguments";
  let target = parse_int Sys.argv.(1) in
  let nums = read_numbers () in
  match two_sum nums target with
  | Some (i, j) -> Printf.printf "%d %d\n" i j
  | None -> print_endline "none"
