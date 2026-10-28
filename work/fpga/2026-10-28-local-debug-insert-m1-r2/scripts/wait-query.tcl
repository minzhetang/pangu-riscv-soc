puts {A_R2_WAIT_QUERY_BEGIN}
puts "A_HAS_INCR=[info commands incr]"
set a_probe_count 0
while {$a_probe_count < 2} {
    after 1
    incr a_probe_count
}
puts "A_BOUNDED_WAIT_COUNT=$a_probe_count"
puts {A_R2_WAIT_QUERY_END}
