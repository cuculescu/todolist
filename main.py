import tkinter as tk
import gui


def main():
    # Creeaza fereastra de baza
    root = tk.Tk()

    # Incarca elementele vizuale din gui.py
    gui.setup_gui(root)

    # Mentine aplicatia deschisa
    root.mainloop()


if __name__ == "__main__":
    main()