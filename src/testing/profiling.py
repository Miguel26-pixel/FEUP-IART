import cProfile
import io
import pstats


def average(stats, count):
    stats.total_calls /= count
    stats.prim_calls /= count
    stats.total_tt /= count

    for func, source in stats.stats.items():
        cc, nc, tt, ct, callers = source
        stats.stats[func] = ( cc/count, nc/count, tt/count, ct/count, callers )

    return stats

def best_of_profillings(target_profile_function, count):
    output_stream = io.StringIO()
    profiller_status = pstats.Stats( stream=output_stream )

    for index in range(count):
        profiller = cProfile.Profile()
        list1 = [random.randint(0,2000) for i in range(0, 1000000)]
        list2 = [random.randint(0,2000) for i in range(0, 500000)]

        network = graph.Graph()

        network.junctions = [graph.Junction((random.randint(1,10000),1)) for i in range(2001)]

        for j in range(0, 2000):
            network.add_street(random.randint(0, 2000), random.randint(0, 2000), 1, 1, bool(random.getrandbits(1)))

        profiller.enable()

        target_profile_function(list1, list2, network)

        profiller.disable()
        profiller_status.add( profiller )

        print( 'Profiled', '%.3f' % profiller_status.total_tt, 'seconds at', index,
                'for', target_profile_function.__name__, flush=True )

    average( profiller_status, count )
    profiller_status.sort_stats( "time" )
    profiller_status.print_stats()

    return "\nProfile results for %s\n%s" % ( 
           target_profile_function.__name__, output_stream.getvalue() )