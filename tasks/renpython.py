from renpybuild.model import task


@task(kind="python", always=True)
def clean(c):
    c.clean()


@task(kind="python", always=True)
def build(c):

    c.run("""{{ CC }} {{ CFLAGS }} -c -o renpython.o {{ source }}/renpython.c """)

    c.run("""
    {{ CC }} {{ LDFLAGS }}
    -o renpython{{ c.python }}
    renpython.o
    -lrenpy
    -l{{ pythonver }}

    -lavformat
    -lavcodec
    -lswscale
    -lswresample
    -lavutil

    -lSDL2_image
    -lSDL2
    -lGLEW
    -lGL
    -ljpeg
    -lpng
    -lwebp
    -lfribidi
    -lfreetype
    -lffi
    -ldl
    -lssl
    -lcrypto
    -lbz2
    -lutil
    -lz
    -lpthread
    -lm
    """)

    c.run("""install renpython{{ c.python }} {{ install }}/bin/renpython{{ c.python }}""")