function soma(x::Int, y::Int)::Int
    a::Int
    a=x+y
    return a
end
function multiplicacao(x::Int, y::Int)::Int
    r::Int
    r=x*y
    return r
end
a::Int
b::Int
c::Int
a=3
b = soma(a, 4)
c = multiplicacao(a, b)
println(b)
println(c)
