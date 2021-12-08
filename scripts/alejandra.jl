using Distributed

using Dates
using DataFrames, StatsPlots, Arrow, DataFramesMeta
using Plots


PROCESSES = Sys.CPU_THREADS
addprocs(PROCESSES)


@everywhere using DrWatson
@everywhere @quickactivate "TD"


@everywhere begin
    include(srcdir("ABM.jl"))
    include(srcdir("constants.jl"))
end


@everywhere function initialize(; n, μ, δ, init_strategy = 50)
    return create_model(Dict{Symbol, Any}(:n => n, :μ => μ, :δ => δ, :init_strategy => init_strategy))
end

### time series

params = Dict(  :n => 100, 
                :μ => collect(1e-2:2e-2:1e-1), 
                :δ => 10
            )

adata, _ = paramscan(params, initialize; 
    agent_step! = player_step!, 
    model_step! = WF_sampling!, 
    n = 1_000, 
    adata = [(:fitness, mean), (:strategy, mean)], 
    parallel = true
    )

@df adata plot(:step, :mean_strategy, group = (:μ), legend = :bottomright, xlabel = "generation", ylabel = "mean claim", dpi = 300)

try
    mkdir(datadir(string(today())))
catch
    @warn "today's directory already exists"
end


Arrow.write(datadir(string(today()), "vary_mu_delta.arrow"), adata)

savefig(current(), plotsdir("vary_mu.png"))


### phase diagram

params = Dict(  :n => 100, 
                :μ => collect(1e-2:5e-3:2e-1), 
                :δ => collect(1:20)
            )

adata, _ = paramscan(params, initialize; 
    agent_step! = player_step!, 
    model_step! = WF_sampling!, 
    n = 1_000, 
    adata = [(:strategy, mean)], 
    parallel = true
    )

begin
    try
        mkdir(datadir(string(today())))
    catch
        @warn "today's directory already exists"
    end
end

Arrow.write(datadir(string(today()), "vary_mu_delta.arrow"), adata)


scatter(
    adata[adata.step .== 1000, :μ], 
    adata[adata.step .== 1000, :δ], 
    marker_z = adata[adata.step .== 1000, :mean_strategy], label = "mean claim at t = 1000",
    markershape = :rect,
    markersize = 10,
    xlabel = "mutation probability μ",
    ylabel = "maximal mutation size δ",
    dpi = 500,
    )

savefig(plotsdir("phase-diagram"))

