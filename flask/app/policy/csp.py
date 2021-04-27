csp = {
    'default-src': [
        '\'self\''
    ],
    'script-src': [
        'https://kit.fontawesome.com/4b9ba14b0f.js',
        'http://localhost:5500/livereload.js',
        'https://use.fontawesome.com/releases/v5.3.1/js/all.js',
        'http://localhost:5000/static/js/base.js',
        'http://localhost:5500/static/js/base.js',
        '\'sha256-MclZcNa5vMtp/wzxRW6+KS3i8mRUf6thpmjT3pkIT5I=\''

    ],
    'style-src': [
        '\'self\'',
        'https://cdnjs.cloudflare.com',
        'https://fonts.googleapis.com/css2',
        'https://ka-f.fontawesome.com/releases/v5.15.3/css/free-v4-font-face.min.css',
        'https://use.fontawesome.com',
        '\'sha256-mCk+PuH4k8s22RWyQ0yVST1TXl6y5diityhSgV9XfOc=\'',
        '\'sha256-Ni2urx9+Bf7ppgnlSfFIqsvlGMFm+9lurWkFfilXQq8=\'',
        '\'sha256-JdCH8SP11p44kp0La4MPFI5qR9musjNwAg5WtqgDI4o=\'',
        '\'sha256-bviLPwiqrYk7TOtr5i2eb7I5exfGcGEvVuxmITyg//c=\'',
        '\'sha256-tUCWndpLW480EWA+8o4oeW9K2GGRBQIDiewZzv/cL4o=\''
    ],
    'connect-src': [
        'https://ka-f.fontawesome.com',
        'ws://localhost:5500/livereload'
    ],
    'font-src': [
        'https://fonts.gstatic.com',
        'https://ka-f.fontawesome.com'
    ],
    'img-src': [
        '\'self\'',
        'data:'
    ],
    'frame-ancestors': 'none'
}