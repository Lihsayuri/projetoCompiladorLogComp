function fatorial(n::Int)::Int
    if (n == 0) || (n == 1)
        return 1
    else
        return n * fatorial(n - 1)
    end
end

resultado::Int
numero::Int
numero = 6
resultado = fatorial(numero)
println(resultado)
