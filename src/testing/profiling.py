import cProfile
import io
import pstats
import random
from utils import graph
from timeit import default_timer as timer


def average(stats, count):
    stats.total_calls /= count
    stats.prim_calls /= count
    stats.total_tt /= count

    for func, source in stats.stats.items():
        cc, nc, tt, ct, callers = source
        stats.stats[func] = (cc/count, nc/count, tt/count, ct/count, callers)

    return stats


def function_time(target_function, count):
    sum = 0

    for i in range(count):
        start = timer()
        target_function()
        end = timer()
        sum += (end-start)

    return sum / count


def profile_solve(target_profile_function, count):
    output_stream = io.StringIO()
    profiller_status = pstats.Stats(stream=output_stream)

    for index in range(count):
        profiller = cProfile.Profile()

        profiller.enable()

        target_profile_function()

        profiller.disable()
        profiller_status.add(profiller)

        print('Profiled', '%.3f' % profiller_status.total_tt, 'seconds at', index,
              'for', target_profile_function.__name__, flush=True)

    average(profiller_status, count)
    profiller_status.sort_stats("time")
    profiller_status.print_stats()

    return "\nProfile results for %s\n%s" % (
           target_profile_function.__name__, output_stream.getvalue())


def profile_crossover(target_profile_function, graph_size, path_size, count):
    output_stream = io.StringIO()
    profiller_status = pstats.Stats(stream=output_stream)

    for index in range(count):
        profiller = cProfile.Profile()
        list1 = [random.randint(0, graph_size) for i in range(0, path_size)]
        list2 = [random.randint(0, graph_size) for i in range(0, path_size)]

        network = graph.Graph()

        for _ in range(graph_size + 1):
            network.add_junction((random.randint(1, 10000), 1))

        for j in range(0, int(graph_size * 1.2)):
            network.add_street(random.randint(0, graph_size), random.randint(
                0, graph_size), 1, 1, bool(random.getrandbits(1)))

        profiller.enable()

        target_profile_function(list1, list2, network)

        profiller.disable()
        profiller_status.add(profiller)

        print('Profiled', '%.3f' % profiller_status.total_tt, 'seconds at', index,
              'for', target_profile_function.__name__, flush=True)

    average(profiller_status, count)
    profiller_status.sort_stats("time")
    profiller_status.print_stats()

    return "\nProfile results for %s\n%s" % (
           target_profile_function.__name__, output_stream.getvalue())
