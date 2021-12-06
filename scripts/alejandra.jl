using Distributed

using Dates
using DataFrames, StatsPlots, Arrow
using Plots


PROCESSES = Sys.CPU_THREADS
addprocs(PROCESSES)


@everywhere using DrWatson
@everywhere @quickactivate "TD"


@everywhere begin
    @quickactivate "TD"
    include(srcdir("ABM.jl"))
    include(srcdir("constants.jl"))
end


@everywhere function initialize(; n, μ, δ, init_strategy = 50)
    return create_model(Dict{Symbol, Any}(:n => n, :μ => μ, :δ => δ, :init_strategy => init_strategy))
end


params = Dict(  :n => 100, 
                :μ => .1, 
                :δ => collect(1:1:10)
            )

adata, _ = paramscan(params, initialize; 
    agent_step! = player_step!, 
    model_step! = WF_sampling!, 
    n = 1_000, 
    adata = [(:fitness, mean), (:strategy, mean)], 
    parallel = true
    )



try 
    mkdir(datadir(string(today())))
catch
    @warn "today's directory already exists"
end


Arrow.write(datadir(string(today()), "vary_mu_delta.arrow"), adata)

@df adata plot(:step, :mean_strategy, group = (:δ), legend = :bottomright, xlabel = "generation", ylabel = "mean claim", dpi = 300)
savefig(current(), plotsdir("vary_mu_delta.png"))