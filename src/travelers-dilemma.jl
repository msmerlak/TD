include(srcdir("constants.jl"))

function π(x, y, model)
    if x > y 
        return min(x, y) - model.punishment
    elseif x < y
        return min(x, y) + model.reward
    else
        return min(x,y)
    end
end