import src.functionsProspecAPI as prospec
from src.arrFiles import main as prep_files


def update_study():
    pass


def create_study(idStudy, nameStudy):
    with open("estudos criados", 'a') as fp:
        fp.write("ID: %d, Nome: %s\n" % (idStudy, nameStudy))

    idStudy = prospec.createStudy(nameStudy, "", 0, 0)

    print("O estudo %s foi criado com ID %d" % (nameStudy, idStudy))


def menu():
    control_flow = input("<criar>, fazer <upload> de arquivos ou <rodar> estudo: ")

    if control_flow == "criar":
        choice = input("Qual o estudo que deseja?\n1- Curtísimo prazo\n2- ONS CP\n3- Matriz CP")
        choice = int(choice)

        if choice == 1:
            idStudy = 0
            nameStudy = "Curtíssimo prazo"

            create_study(idStudy, nameStudy)

        elif choice < 4:
            print("Opção em implementação.")

        else:
            print("Opção inválida.")

    elif control_flow == "upload":
        print("Esses são os estudos criados até então:")
        with open("estudos criados", 'r') as fp:
            for line in fp:
                print(line)

        int(input("Para qual estudo deseja enviar os arquivos?\n"))
        prep_files()

    else:
        print("Programa encerrado.")


def main():
    prospec.authenticateProspec("daniel.mazucanti@skoposenergia.com.br", "Skopos2020")

    numRequests = prospec.getNumberOfRequests()

    print("Foram feitas %s requisições até o momento." % numRequests)

    menu()


main()
