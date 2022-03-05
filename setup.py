from distutils.core import setup, Extension

def main():
    setup(name="med",
          version="1.0.0",
          description="Python interface for fast calculation of minimum edit distance",
          author="Waldemar Kolodziejczyk",
          author_email="kolodziejczykwaldemar222@gmail.com",
          ext_modules=[Extension("med", ["min_edit_distance.c"])])

if __name__ == "__main__":
    main()
