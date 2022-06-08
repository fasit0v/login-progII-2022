import json
import ttkbootstrap as ttk
from werkzeug.security import check_password_hash,generate_password_hash
from tkinter import messagebox as ms
import funciones as fn
from menuCompras import Compras
from menuDeposito import Deposito
from menuEmpleados import Empleados
from menuVentas import Ventas


pantalla = ttk.Window()
pantalla.title("Login de usuarios")
pantalla.geometry("400x300")

#Recordar contraseña
lstRecordar = fn.abrirArchivo("recordarme.json")
nombre= lstRecordar[0]["Usuario"]
guardar = lstRecordar[0]["Guardar"]


#variables
varNombre = ttk.StringVar(pantalla,nombre)
varContra = ttk.StringVar(pantalla,"")
varRecordar = ttk.BooleanVar(pantalla,guardar) 

#funciones
def recordar():
    if varRecordar.get():
        lstRecordar[0]["Usuario"]= varNombre.get()
        lstRecordar[0]["Recordar"] = True
    else:
        lstRecordar[0]["Usuario"]= ""
        lstRecordar[0]["Recordar"] = False
    with open("recordarme.json","w") as recordar:
        json.dump(lstRecordar,recordar)

def login():
    if len(varContra.get()) > 0 and len(varNombre.get()) > 0:
        lstUsuario = fn.abrirArchivo("archivosJSON/usuarios.json")
        encontrado = False 
        for i in lstUsuario:
            if i["Usuario"] == (varNombre.get()).upper() and check_password_hash(i["Contra"],varContra.get()):
                encontrado = True
                global idBuscar
                idBuscar = i["IDUsuario"]
                inicio = i["Inicio"]
                break
        if encontrado:
            if inicio:
                recordar()
                lstEmpleado = fn.abrirArchivo("archivosJSON/empleados.json")
                for i in lstEmpleado:
                    if i["IDEmpleado"] == idBuscar:
                        if i["Sector"] == "Deposito":
                            Deposito()
                        elif i["Sector"] == "Empleados":
                            Empleados()
                        elif i["Sector"] == "Compras":
                            Compras()
                        elif i["Sector"] == "Ventas":
                            Ventas()
                        break
            else:
                global cambiar  
                try:
                    if cambiar.state() == "normal":
                        cambiar.focus()
                except:
                    cambiar = ttk.Toplevel(title="Formulario")
                    cambiar.geometry("600x400")

                    #variable
                    varNueva = ttk.StringVar(cambiar,"")
                    varRepetir = ttk.StringVar(cambiar,"")
                    
                    def confirmarContra():
                        if varNueva.get() != "" and varRepetir.get() != ""  and varRepetir.get() == varNueva.get():
                            lstUsuario = fn.abrirArchivo("archivosJSON/usuarios.json")
                            for i in lstUsuario:
                                if i["IDUsuario"] == idBuscar:
                                    i["Contra"] = generate_password_hash(varNueva.get())
                                    i["Inicio"] =True
                            cambiar.destroy()
                            ms.showinfo("Operacion realizada","El cambio de contraseña se ha realizado correctamente. Por favor ingrese nuevamente")
                            with open("archivosJSON/usuarios.json","w") as archivo:
                                json.dump(lstUsuario,archivo)
                        else:
                            if varNueva.get() == "" or varRepetir.get() == "":
                                ms.showerror("Error","Las casillas no pueden estar vacias")
                            elif varRepetir.get() != varNueva.get():
                                ms.showerror("Error","Repita correctamente la contraseña")
                            cambiar.focus()
                    #estructura
                    ttk.Label(cambiar,text="Ingrese contraseña").place(x=20,y=40)
                    ttk.Entry(cambiar,textvariable=varNueva).place(x=210,y=40)

                    ttk.Label(cambiar,text="Repetir contraseña").place(x=20,y=100)
                    ttk.Entry(cambiar,textvariable=varRepetir).place(x=210,y=100)

                    #btn confirmar
                    ttk.Button(cambiar,text="confirmar",command=confirmarContra).place(x=210,y=160)
        else:
            ms.showinfo("Usuario no encontrado","El usuario o la contraseña no son correctas")
    else:
        ms.showerror("Error","Ingrese la informacion necesaria")


#Nombre
ttk.Label(pantalla,text="Nombre").place(x=20,y=20)
entNombre = ttk.Entry(pantalla,textvariable=varNombre)
entNombre.place(x=150,y=20)

#contra
ttk.Label(pantalla,text="Contra").place(x=20,y=80)
entContra = ttk.Entry(pantalla,textvariable=varContra)
entContra.place(x=150,y=80)

#Recordarme
ttk.Checkbutton(pantalla,text="Recordarme",variable=varRecordar,offvalue=False,onvalue=True).place(x=130,y=130)

#buton cargar datos
btnCargar = ttk.Button(pantalla,command=login,text="Loguear")
btnCargar.place(x=150,y=180)

#Inciar
pantalla.mainloop()