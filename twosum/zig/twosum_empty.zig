// Two Sum : trouver deux indices i < j tels que nums[i] + nums[j] == target.
// Écrit pour Zig 0.15.
const std = @import("std");

const usage = "usage: twosum <target>   (nombres lus sur stdin)";
const limit: i64 = 1_000_000_000_000_000_000;

pub const Pair = struct { i: usize, j: usize };

/// Renvoie .{ .i, .j } avec i < j et nums[i] + nums[j] == target, ou null.
/// S'il y a plusieurs solutions : le plus petit j, puis le plus petit i.
/// Doit être en O(n).
fn twoSum(allocator: std.mem.Allocator, nums: []const i64, target: i64) !?Pair {
    // TODO
    _ = allocator;
    _ = nums;
    _ = target;
    return error.Todo;
}

fn die(comptime fmt: []const u8, args: anytype) noreturn {
    std.debug.print("error: " ++ fmt ++ "\n" ++ usage ++ "\n", args);
    std.process.exit(1);
}

fn parseInt(s: []const u8) i64 {
    const digits = if (s.len > 0 and s[0] == '-') s[1..] else s;
    if (digits.len == 0) die("invalid number '{s}'", .{s});
    for (digits) |c| {
        if (c < '0' or c > '9') die("invalid number '{s}'", .{s});
    }
    const n = std.fmt.parseInt(i64, s, 10) catch die("number out of range '{s}'", .{s});
    if (n > limit or n < -limit) die("number out of range '{s}'", .{s});
    return n;
}

pub fn main() !void {
    var gpa: std.heap.GeneralPurposeAllocator(.{}) = .init;
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const args = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, args);
    if (args.len != 2) die("wrong number of arguments", .{});
    const target = parseInt(args[1]);

    const input = try std.fs.File.stdin().readToEndAlloc(allocator, 1 << 30);
    defer allocator.free(input);

    var nums: std.ArrayList(i64) = .empty;
    defer nums.deinit(allocator);
    var it = std.mem.tokenizeAny(u8, input, " \t\r\n\x0c");
    while (it.next()) |tok| try nums.append(allocator, parseInt(tok));

    var buf: [64]u8 = undefined;
    const out = if (try twoSum(allocator, nums.items, target)) |p|
        try std.fmt.bufPrint(&buf, "{d} {d}\n", .{ p.i, p.j })
    else
        "none\n";
    try std.fs.File.stdout().writeAll(out);
}
