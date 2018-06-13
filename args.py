from sys import argv


def get_opts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':  # detect "-name value" pair.
            if len(argv) > 1:
                opts[argv[0]] = argv[1]
        argv = argv[1:]  # Remove unnecessary parameter
    return opts


#
#  get command-line arguments for crawler.py
#
def args_crawler(argv):
    opts = get_opts(argv)
    args = {
        'lon': None,
        'lat': None,
    }
    try:
        if '-lon' in opts:
            args['lon'] = float(opts['-lon'])
        if '-lat' in opts:
            args['lat'] = float(opts['-lat'])
    except ValueError as errno:
        print('Value error: {0}'.format(errno))
        print('Usage: python crawler.py -lon <longitude> -lat <latitude>')
    return args


#
#  get command-line arguments for query.py
#
def args_query(argv):
    opts = get_opts(argv)
    args = {'lon': None, 'lat': None, 'radius': 0, 'keyword': None}
    try:
        if '-lon' in opts:
            args['lon'] = float(opts['-lon'])
        if '-lat' in opts:
            args['lat'] = float(opts['-lat'])
        if '-r' in opts:
            args['radius'] = float(opts['-r'])
        if '-k' in opts:
            args['keyword'] = opts['-k']
    except ValueError as errno:
        print('Value error: {0}'.format(errno))
        print(
            'Usage: python query.py -k <keywords> -lon <longitude> -lat <latitude> -r <radius>'
        )
    return args
