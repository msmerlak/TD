using Distributed

PROCESSES = Sys.CPU_THREADS - 2
addprocs(PROCESSES)

@everywhere begin
    import Pkg
    Pkg.activate(".") 
end

@everywhere using DrWatson

using DataFrames, StatsPlots, Arrow, DataFramesMeta
using Statistics

@everywhere begin
    include(srcdir("ABM.jl"))
    include(srcdir("constants.jl"))
end


@everywhere function initialize(; 
    n = 100, 
    μ = .1, 
    δ = 5, 
    init_strategy = 2, 
    β = 1,
    reward = 2, 
    punishment = 2
    )
    return create_model(Dict{Symbol, Any}(:n => n, :μ => μ, :δ => δ, :init_strategy => init_strategy, :β => β, :reward => reward, :punishment => punishment))
end

P = Dict(  :n => 100, 
                :μ => .1,#collect(1e-2:1e-1:1), 
                :reward => 2,
                :β => 10.,
                :punishment => 2,
                :δ => collect(10:10:60)
            )

adata, _ = paramscan(P, initialize; 
    agent_step! = player_step!, 
    model_step! = WF_sampling!, 
    n = 5_000, 
    adata = [(:fitness, mean), (:strategy, mean)], 
    parallel = true
    )

@df adata plot(:step, :mean_strategy, group = (:δ), legend = :bottomright, xlabel = "generation", ylabel = "mean claim", dpi = 300, title = "Wright-Fisher (N = $(P[:n]), β = $(P[:β]), μ = $(P[:μ]), varying δ)")
