from project import project

def main():
    try:
        project.run(debug = True)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()