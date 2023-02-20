import shutil


def replace_conf_file(ssid, password):
    shutil.copyfile("client.conf", "client_copy.conf")
    with open("client.conf", "w+") as file:
        file.write("ctrl_interface=wpaspy_ctrl\n")
        file.write("sae_pwe=2\n")
        file.write("network={\n")
        file.write(f"    ssid=\"{ssid}\"\n")
        file.write(f"    psk=\"{password}\"\n")
        file.write("\n")
        file.write("    pairwise=CCMP\n")
        file.write("\n")
        file.write("}\n")
        file.close()