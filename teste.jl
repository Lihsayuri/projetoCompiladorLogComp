i::Int
n::Int
f::Int
n = 5
i = 2
f = 1
while i < n + 1
    if i == 4
        println("i = 4")
    end
    f = f * i
    i = i + 1
end
println(f)
