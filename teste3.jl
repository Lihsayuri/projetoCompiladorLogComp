function countdown(n::Int)::Int
    if n == 0
        println(42)
    else
        println(n)
        countdown(n - 1)
    end
    return 0
end

countdown(5)
