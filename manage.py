from project import project

def main():
    try:
        project.run(debug = True, port = 5001)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()  
