import os, sys
import random
import json
import webbrowser

from customtkinter import *
from tkinter import filedialog, messagebox
from PIL import Image

import elgamal

cwd = os.getcwd()


class CustomLabel(CTkLabel):
    def __init__(self, master, font_size=14, *args, **kwargs):
        CTkLabel.__init__(self, master, font_size, *args, **kwargs)
        self.configure(
            bg_color=("#ffffff", "#2b2b2b"), font=("arial", font_size, "bold")
        )


class App(CTk):
    def __init__(self):
        super().__init__()
        self.mode, self.theme, self.mode_text = self.get_mode()

        self.load_icons()
        self.cre_tab_view()
        self.cre_btn_change_mode()
        self.short_cuts()

    def load_icons(self):
        self.img_mode = CTkImage(
            Image.open("data/images/light.png"),
            Image.open("data/images/dark.png"),
            size=(30, 30),
        )
        self.img_key = CTkImage(Image.open("data/images/key.png"), size=(20, 20))
        self.img_clean = CTkImage(Image.open("data/images/clean.png"), size=(20, 20))
        self.img_exit = CTkImage(Image.open("data/images/exit.png"), size=(20, 20))
        self.img_open_file = CTkImage(
            Image.open("data/images/openfile.png"), size=(20, 20)
        )
        self.img_ky = CTkImage(Image.open("data/images/ky.png"), size=(20, 20))
        self.img_forward = CTkImage(
            Image.open("data/images/forward.png"), size=(20, 20)
        )
        self.img_save_file = CTkImage(
            Image.open("data/images/save-file.png"), size=(20, 20)
        )
        self.img_check = CTkImage(Image.open("data/images/check.png"), size=(20, 20))
        self.img_mess = CTkImage(Image.open("data/images/mess.png"), size=(23, 23))
        self.img_dog = CTkImage(Image.open("data/images/dog.png"), size=(500, 411))

    def short_cuts(self):
        self.bind("<Control-d>", self.change_mode)
        self.bind("<Control-D>", self.change_mode)
        self.bind("<Control-s>", self.save_file_ck1)
        self.bind("<Control-S>", self.save_file_ck1)
        self.bind("<Control-f>", self.forward_data)
        self.bind("<Control-F>", self.forward_data)
        self.bind("<Control-r>", self.clean_data)
        self.bind("<Control-R>", self.clean_data)
        self.bind("<Control-e>", self.fake_data)
        self.bind("<Control-E>", self.fake_data)
        self.bind("<Control-o>", self.open_file_edit)
        self.bind("<Control-O>", self.open_file_edit)
        self.bind("<Key>", self.change_theme)

    def cre_btn_change_mode(self):
        self.hot_keys = {
            113: "green",
            112: "blue",
            114: "red",
            115: "pink",
            116: "custom1",
            117: "custom2",
            118: "custom3",
            119: "custom4",
            120: "custom5",
        }

        self.btn_change_mode = CTkButton(
            self,
            text=self.mode_text,
            width=27,
            height=27,
            fg_color=("#ebebeb", "#242424"),
            hover_color=("#ebebeb", "#242424"),
            text_color=("#000000", "#ffffff"),
            font=("arial", 13, "bold"),
            image=self.img_mode,
            command=lambda: self.change_mode(event=None),
        )
        self.btn_change_mode.place(x=1202, y=10)

    def cre_tab_view(self):
        self.tab_view = CTkTabview(
            self, width=1317, height=580, fg_color=("#ebebeb", "#242424")
        )
        self.tab_view.place(x=10, y=5)

        self.tab_dig_sign = "Chữ ký số điện tử - Elgamal"

        self.tab_view.add(self.tab_dig_sign)
        self.tab_view.set(self.tab_dig_sign)

        self.cre_tab_dig_sign()

    def cre_tab_dig_sign(self):
        """Tab 1  - Chữ ký số"""
        self.tab1 = self.tab_view.tab(self.tab_dig_sign)

        """Frame Tạo Khóa """
        self.frame_gen_key = CTkFrame(
            master=self.tab1, width=425, height=520, fg_color=("#ffffff", "#2b2b2b")
        )
        self.frame_gen_key.place(x=0, y=10)
        # [p, alpha, a, beta, k, gamal]
        # α, β, γ
        CustomLabel(master=self.frame_gen_key, text="TẠO KHÓA").place(x=15, y=10)
        CustomLabel(master=self.frame_gen_key, text="Khóa công khai (p, α, β):").place(
            x=20, y=45
        )
        CustomLabel(master=self.frame_gen_key, text="Số nguyên tố p =").place(
            x=40, y=80
        )
        CustomLabel(master=self.frame_gen_key, text="Số (alpha) α =").place(x=40, y=130)
        CustomLabel(master=self.frame_gen_key, text="Số β = α^a mod p =").place(
            x=40, y=180
        )

        CustomLabel(master=self.frame_gen_key, text="Khóa bí mật (a):").place(
            x=20, y=230
        )
        CustomLabel(master=self.frame_gen_key, text="Số nguyên a =").place(x=40, y=265)
        CustomLabel(master=self.frame_gen_key, text="Số ngẫu nhiên k =").place(
            x=40, y=315
        )
        CustomLabel(master=self.frame_gen_key, text="Số γ = α^k mod p =").place(
            x=40, y=365
        )

        self.entry_p = CTkEntry(
            master=self.frame_gen_key,
            placeholder_text="số nguyên tố p",
            font=("arial", 13, "bold"),
            width=180,
            height=35,
        )
        self.entry_p.place(x=200, y=78)

        self.entry_alpha = CTkEntry(
            master=self.frame_gen_key,
            placeholder_text="số nguyên alpha",
            font=("arial", 13, "bold"),
            width=180,
            height=35,
        )
        self.entry_alpha.place(x=200, y=128)

        self.entry_beta = CTkEntry(
            master=self.frame_gen_key,
            placeholder_text="số nguyên beta",
            font=("arial", 13, "bold"),
            width=180,
            height=35,
        )
        self.entry_beta.place(x=200, y=178)

        self.entry_a = CTkEntry(
            master=self.frame_gen_key,
            placeholder_text="số nguyên a",
            font=("arial", 13, "bold"),
            width=180,
            height=35,
        )
        self.entry_a.place(x=200, y=263)

        self.entry_k = CTkEntry(
            master=self.frame_gen_key,
            placeholder_text="số nguyên k",
            font=("arial", 13, "bold"),
            width=180,
            height=35,
        )
        self.entry_k.place(x=200, y=313)

        self.entry_gamal = CTkEntry(
            master=self.frame_gen_key,
            placeholder_text="số nguyên gamal",
            font=("arial", 13, "bold"),
            width=180,
            height=35,
        )
        self.entry_gamal.place(x=200, y=363)

        CTkButton(
            master=self.frame_gen_key,
            text="Tạo khóa ngẫu nhiên",
            width=380,
            height=35,
            bg_color=("#ffffff", "#2b2b2b"),
            font=("arial", 13, "bold"),
            image=self.img_key,
            command=self.gen_key,
        ).place(x=23, y=423)

        CTkButton(
            master=self.frame_gen_key,
            text="Reset dữ liệu",
            width=185,
            height=35,
            bg_color=("#ffffff", "#2b2b2b"),
            font=("arial", 13, "bold"),
            image=self.img_clean,
            command=lambda: self.clean_data(event=None),
        ).place(x=23, y=470)

        CTkButton(
            master=self.frame_gen_key,
            text="Thoát",
            width=185,
            height=35,
            bg_color=("#ffffff", "#2b2b2b"),
            font=("arial", 13, "bold"),
            image=self.img_exit,
            command=self.thoat,
        ).place(x=219, y=470)

        """Frame Ký Văn Bản"""
        self.ky_frame = CTkFrame(
            master=self.tab1, width=425, height=520, fg_color=("#ffffff", "#2b2b2b")
        )
        self.ky_frame.place(x=440, y=10)

        CustomLabel(master=self.ky_frame, text="PHÁT SINH CHỮ KÝ").place(x=15, y=10)
        CustomLabel(master=self.ky_frame, text="Chọn file văn bản:").place(x=23, y=45)
        CustomLabel(master=self.ky_frame, text="Nội dung văn bản:").place(x=23, y=120)
        CustomLabel(master=self.ky_frame, text="Hàm băm:").place(x=23, y=220)
        CustomLabel(master=self.ky_frame, text="Nội dung chữ ký:").place(x=23, y=268)
        

        self.entry_file_vb1 = CTkEntry(
            master=self.ky_frame,
            placeholder_text="đường dẫn file văn bản",
            font=("arial", 13, "bold"),
            width=270,
            height=35,
        )
        self.entry_file_vb1.place(x=23, y=78)

        CTkButton(
            master=self.ky_frame,
            text="Mở file",
            width=100,
            height=35,
            bg_color=("#ffffff", "#2b2b2b"),
            font=("arial", 13, "bold"),
            image=self.img_open_file,
            command=self.open_file_vb1,
        ).place(x=303, y=78)

        self.textbox_nd1 = CTkTextbox(
            master=self.ky_frame,
            width=380,
            height=50,
            border_width=1,
            font=("arial", 13, "bold"),
        )
        self.textbox_nd1.place(x=23, y=155)

        self.textbox_hash1 = CTkTextbox(
            master=self.ky_frame,
            width=300,
            height=30,
            border_width=1,
            font=("arial", 13, "bold"),
        )
        self.textbox_hash1.place(x=100, y=220)

        self.textbox_ck1 = CTkTextbox(
            master=self.ky_frame,
            width=380,
            height=103,
            border_width=1,
            font=("arial", 13, "bold"),
        )
        self.textbox_ck1.place(x=23, y=305)

        self.cbx_hash = CTkComboBox(
            master=self.ky_frame,
            values=["MD5"],
            font=("arial", 14, "bold"),
            cursor="hand2",
            bg_color=("#ffffff", "#2b2b2b"),
            width=105,
            state="readonly",
        )
        self.cbx_hash.place(x=298, y=268)
        self.cbx_hash.set("MD5")
        # CTkComboBox -> DropdownMenu -> min_character_width = 5

        CTkButton(
            master=self.ky_frame,
            text="Tiến hành ký văn bản",
            width=380,
            height=35,
            bg_color=("#ffffff", "#2b2b2b"),
            font=("arial", 13, "bold"),
            image=self.img_ky,
            command=self.gen_sign,
        ).place(x=23, y=423)

        CTkButton(
            master=self.ky_frame,
            text="Chuyển tiếp dữ liệu",
            width=185,
            height=35,
            bg_color=("#ffffff", "#2b2b2b"),
            font=("arial", 13, "bold"),
            image=self.img_forward,
            command=lambda: self.forward_data(event=None),
        ).place(x=23, y=470)

        CTkButton(
            master=self.ky_frame,
            text="Lưu file chữ ký",
            width=185,
            height=35,
            bg_color=("#ffffff", "#2b2b2b"),
            font=(
                "arial",
                13,
                "bold",
            ),
            image=self.img_save_file,
            command=lambda: self.save_file_ck1(event=None),
        ).place(x=219, y=470)

        """Frame Kiểm Tra Chữ Ký"""
        self.check_frame = CTkFrame(
            master=self.tab1, width=425, height=520, fg_color=("#ffffff", "#2b2b2b")
        )
        self.check_frame.place(x=880, y=10)

        CustomLabel(master=self.check_frame, text="KIỂM TRA CHỮ KÝ").place(x=15, y=10)
        CustomLabel(master=self.check_frame, text="Chọn file văn bản kiểm tra:").place(
            x=23, y=45
        )
        CustomLabel(master=self.check_frame, text="Nội dung văn bản:").place(
            x=23, y=120
        )
        CustomLabel(master=self.check_frame, text="Hàm băm:").place(x=23, y=220)
        CustomLabel(master=self.check_frame, text="Chọn file chữ ký:").place(
            x=23, y=255
        )
        CustomLabel(master=self.check_frame, text="Nội dung chữ ký:").place(x=23, y=330)

        self.entry_file_vb2 = CTkEntry(
            master=self.check_frame,
            placeholder_text="đường dẫn file văn bản",
            font=("arial", 13, "bold"),
            width=270,
            height=35,
        )
        self.entry_file_vb2.place(x=23, y=78)

        CTkButton(
            master=self.check_frame,
            text="Mở file",
            width=100,
            height=35,
            bg_color=("#ffffff", "#2b2b2b"),
            font=("arial", 13, "bold"),
            image=self.img_open_file,
            command=self.open_file_vb2,
        ).place(x=303, y=78)

        self.entry_file_ck2 = CTkEntry(
            master=self.check_frame,
            placeholder_text="đường dẫn file chữ ký",
            font=("arial", 13, "bold"),
            width=270,
            height=35,
        )
        self.entry_file_ck2.place(x=23, y=290)

        CTkButton(
            master=self.check_frame,
            text="Mở file",
            width=100,
            height=35,
            bg_color=("#ffffff", "#2b2b2b"),
            font=("arial", 13, "bold"),
            image=self.img_open_file,
            command=self.open_file_ck2,
        ).place(x=303, y=290)

        self.textbox_nd2 = CTkTextbox(
            master=self.check_frame,
            width=380,
            height=50,
            border_width=1,
            font=("arial", 13, "bold"),
        )
        self.textbox_nd2.place(x=23, y=155)

        self.textbox_hash2 = CTkTextbox(
            master=self.check_frame,
            width=300,
            height=30,
            border_width=1,
            font=("arial", 13, "bold"),
        )
        self.textbox_hash2.place(x=100, y=220)

        self.textbox_ck2 = CTkTextbox(
            master=self.check_frame,
            width=380,
            height=90,
            border_width=1,
            font=("arial", 13, "bold"),
        )
        self.textbox_ck2.place(x=23, y=365)

        CTkButton(
            master=self.check_frame,
            text="Tiến hành kiểm tra chữ ký",
            width=380,
            height=35,
            bg_color=("#ffffff", "#2b2b2b"),
            font=("arial", 13, "bold"),
            image=self.img_check,
            command=self.check_sign,
        ).place(x=23, y=470)
        

    def get_mode(self):
        try:
            with open(r"data\mode\mode.json", "r") as f:
                data = json.load(f)
            f.close()
            mode = data["mode"]
            theme = data["theme"]
            mode_text = "Light Mode" if mode == "light" else "Dark Mode"
        except:
            mode = "light"
            mode_text = "Light Mode"
            theme = "blue"
        set_appearance_mode(mode)
        set_default_color_theme(f"data/themes/{theme}.json")

        return mode, theme, mode_text

    def write_theme(self, themez):
        data = {"mode": self.mode, "theme": themez}
        try:
            with open(r"data\mode\mode.json", "w") as outfile:
                json.dump(data, outfile)
            outfile.close()
        except FileNotFoundError:
            os.makedirs("data/mode")
            self.write_theme(themez)

    def change_mode(self, event):
        if self.mode == "light":
            set_appearance_mode("dark")
            self.btn_change_mode.configure(text="Dark Mode")
            self.mode = "dark"
        else:
            set_appearance_mode("light")
            self.btn_change_mode.configure(text="Light Mode")
            self.mode = "light"
        self.write_theme(self.theme)

    def change_theme(self, event):
        if event.keycode in self.hot_keys:
            self.theme = self.hot_keys[event.keycode]
            self.write_theme(self.theme)
            python = sys.executable
            os.execl(python, python, *sys.argv)

    def clean_key(self):
        self.entry_p.delete("0", END)
        self.entry_alpha.delete("0", END)
        self.entry_beta.delete("0", END)
        self.entry_a.delete("0", END)
        self.entry_k.delete("0", END)
        self.entry_gamal.delete("0", END)

    def clean_data(self, event):
        self.clean_key()
        self.entry_file_vb1.delete("0", END)
        self.entry_file_vb2.delete("0", END)
        self.entry_file_ck2.delete("0", END)
        self.textbox_hash1.delete("1.0", END)
        self.textbox_nd1.delete("1.0", END)
        self.textbox_nd2.delete("1.0", END)
        self.textbox_hash2.delete("1.0", END)
        self.textbox_ck1.delete("1.0", END)
        self.textbox_ck2.delete("1.0", END)

    def gen_key(self):
        data = elgamal.cre_key()
        self.clean_key()
        self.entry_p.insert("0", data[0])
        self.entry_alpha.insert("0", data[1])
        self.entry_a.insert("0", data[2])
        self.entry_beta.insert("0", data[3])
        self.entry_k.insert("0", data[4])
        self.entry_gamal.insert("0", data[5])

    def check_key(self):
        try:
            p = int(self.entry_p.get())
            alpha = int(self.entry_alpha.get())
            beta = int(self.entry_beta.get())
            a = int(self.entry_a.get())
            k = int(self.entry_k.get())
            gamal = int(self.entry_gamal.get())

            if not elgamal.check_prime(p):
                flag = messagebox.askyesno(
                    "Lỗi!",
                    "Số p cần là số nguyên tố!\nBạn có muốn tạo ngẫu nhiên p không?",
                )
                if flag:
                    self.entry_p.delete("0", END)
                    self.entry_p.insert("0", elgamal.find_prime())
                    return self.check_key()
                else:
                    return

            if a < 2 or a > p - 2:
                flag = messagebox.askyesno(
                    "Lỗi!",
                    "Số a cần thuộc đoạn [2, p - 2]\nBạn có muốn tạo ngẫu nhiên a không?",
                )
                if flag:
                    self.entry_a.delete("0", END)
                    self.entry_a.insert("0", elgamal.gen_a(p))
                    return self.check_key()
                else:
                    return

            if alpha < 2 or alpha > p - 2:
                flag = messagebox.askyesno(
                    "Lỗi!",
                    "Số alpha cần thuộc đoạn [2, p - 1]\nBạn có muốn tạo ngẫu nhiên alpha không?",
                )
                if flag:
                    self.entry_alpha.delete("0", END)
                    self.entry_alpha.insert("0", elgamal.gen_alpha(p))
                    return self.check_key()
                else:
                    return

            if elgamal.find_gcd(k, p - 1) != 1 or k < 1 or k > p - 2:
                flag = messagebox.askyesno(
                    "Lỗi!",
                    "Số k cần thuộc đoạn [1, p - 2] và gcd(k, p - 1) = 1\nBạn có muốn tạo ngẫu nhiên k không?",
                )
                if flag:
                    self.entry_k.delete("0", END)
                    self.entry_k.insert("0", elgamal.gen_k(p))
                    return self.check_key()

            if beta != elgamal.pow_mod(alpha, a, p):
                flag = messagebox.askyesno(
                    "Lỗi!",
                    "Beta chưa chính xác beta = alpha^a mod p\nBạn có muốn cập nhật tự động beta không?",
                )
                if flag:
                    self.entry_beta.delete("0", END)
                    self.entry_beta.insert("0", elgamal.pow_mod(alpha, a, p))
                    return self.check_key()
                else:
                    return

            if gamal != elgamal.pow_mod(alpha, k, p):
                flag = messagebox.askyesno(
                    "Lỗi!",
                    "Gamal chưa chính xác gamal = alpha^k mod p\nBạn có muốn cập nhật tự động gamal không?",
                )
                if flag:
                    self.entry_gamal.delete("0", END)
                    self.entry_gamal.insert("0", elgamal.pow_mod(alpha, k, p))
                    return self.check_key()
                else:
                    return

            return [p, alpha, a, beta, k, gamal]
        except ValueError:
            return ("Lỗi!", "Vui lòng kiểm tra lại kiểu dữ liệu của khóa!")

    def open_file_vb1(self):
        file_url = filedialog.askopenfilename(
            initialdir=cwd, title="Mở file văn bản"
        ).strip()
        if file_url == "":
            return
        self.entry_file_vb1.delete("0", END)
        self.entry_file_vb1.insert("0", file_url)
        self.textbox_nd1.delete("1.0", END)
        try:
            data = elgamal.get_data_file(file_url)
            self.textbox_nd1.insert("1.0", data)
        except:
            messagebox.showerror("Lỗi", "Định dạng file không xác định!")
            self.entry_file_vb1.delete("0", END)
            self.textbox_ck1.delete("1.0", END)

    def open_file_vb2(self):
        file_url = filedialog.askopenfilename(
            initialdir=cwd, title="Mở file văn bản"
        ).strip()
        if file_url == "":
            return
        self.entry_file_vb2.delete("0", END)
        self.entry_file_vb2.insert("0", file_url)
        self.textbox_nd2.delete("1.0", END)
        try:
            data = elgamal.get_data_file(file_url)
            self.textbox_nd2.insert("1.0", data)
        except:
            messagebox.showerror("Lỗi", "Định dạng file không xác định!")
            self.entry_file_vb2.delete("0", END)

    def open_file_ck2(self):
        file_url = filedialog.askopenfilename(
            initialdir=cwd, title="Mở file chữ ký"
        ).strip()
        if file_url == "":
            return
        self.entry_file_ck2.delete("0", END)
        self.entry_file_ck2.insert("0", file_url)
        self.textbox_ck2.delete("1.0", END)
        try:
            data = elgamal.get_data_file(file_url)
            self.textbox_ck2.insert("1.0", data)
        except:
            messagebox.showerror("Lỗi", "Định dạng file không xác định!")
            self.entry_file_ck2.delete("0", END)

    def gen_sign(self):
        keys = self.check_key()
        if "tuple" in str(type(keys)):
            return messagebox.showerror(keys[0], keys[1])

        try:
            [p, alpha, a, beta, k, gamal] = keys
        except TypeError:
            return

        mode_hash = self.cbx_hash.get()
        text = self.textbox_nd1.get("1.0", END).strip()
        if not text:
            return messagebox.showwarning("Lỗi", "Không để trường nội dung trống!")

        sign = elgamal.create_sign(text, mode_hash, gamal, a, k, p)

        self.textbox_ck1.delete("1.0", END)
        self.textbox_ck1.insert("1.0", str(sign[0]))
        self.textbox_hash1.delete("1.0", END)
        self.textbox_hash1.insert("1.0", str(sign[1]))

    def forward_data(self, event):
        noi_dung_vb = self.textbox_nd1.get("1.0", END).strip()
        noi_dung_ck = self.textbox_ck1.get("1.0", END).strip()
        noi_dung_hash = self.textbox_hash1.get("1.0", END).strip()

        if not noi_dung_vb and not noi_dung_ck:
            return messagebox.showwarning("Lỗi!", "Không có nội dung để chuyển tiếp!")

        self.textbox_nd2.delete("1.0", END)
        self.textbox_nd2.insert("1.0", noi_dung_vb)

        self.textbox_hash2.delete("1.0", END)
        self.textbox_hash2.insert("1.0", noi_dung_hash)

        self.textbox_ck2.delete("1.0", END)
        self.textbox_ck2.insert("1.0", noi_dung_ck)

    def save_file_ck1(self, event):
        data = self.textbox_ck1.get("1.0", END).strip()
        if data:
            file_path = filedialog.asksaveasfilename(
                initialdir=cwd,
                title="Lưu file chữ ký",
                filetypes=(("Text Files", "*.txt"),),
                defaultextension=".txt",
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(data)
                f.close()
                messagebox.showinfo(
                    "Thông báo!", "Lưu file thành công!" + "\n" + file_path
                )
            else:
                return None
        else:
            messagebox.showwarning("Lỗi!", "Chưa có nội dung chữ ký!")

    def open_file_edit(self, event):
        url_file = self.entry_file_vb2.get().strip()
        if url_file:
            try:
                os.startfile(url_file)
            except FileNotFoundError:
                messagebox.showwarning("Lỗi!", "Không tìm thấy file!")
        else:
            messagebox.showwarning("Lỗi!", "Chưa có đường dẫn!")

    def check_sign(self):
        mode_hash = self.cbx_hash.get()
        text = self.textbox_nd2.get("1.0", END).strip()
        sign = self.textbox_ck2.get("1.0", END).strip()

        if not text or not sign:
            return messagebox.showwarning(
                "Lỗi", "Không để trường nội dung/chữ ký trống!"
            )

        keys = self.check_key()

        if "tuple" in str(type(keys)):
            return messagebox.showerror(keys[0], keys[1])

        [p, alpha, a, beta, k, gamal] = keys

        try:
            is_sign = elgamal.verify_sign(text, mode_hash, sign, beta, gamal, alpha, p)
        except:
            return messagebox.showerror("Thông báo!", "Lỗi định dạng chữ ký!")

        if is_sign:
            messagebox.showinfo("Thông báo!", "Chữ ký khớp, văn bản không bị thay đổi!")
        else:
            messagebox.showerror(
                "Thông báo!", "Chữ ký không khớp hoặc văn bản đã bị thay đổi!"
            )

    def fake_data(self, event):
        contents = [
            "Chữ ký số Elgamal",
            "Ths Trần Phương Nhung",
            "Trần Đình Đức - 2021602724",
            "An toàn và bảo mật thông tin",
        ]

        self.gen_key()
        self.textbox_nd1.delete("1.0", END)

        self.textbox_nd1.insert("1.0", random.choice(contents))
        self.gen_sign()
        self.forward_data(event=None)
        self.check_sign()

    def thoat(self):
        is_exit = messagebox.askyesno("Thông báo", "Bạn có muốn thoát không?")
        if is_exit:
            self.quit()


if __name__ == "__main__":
    app = App()
    app.title("ElGamal")
    app.iconbitmap(f"data/images/icon.ico")
    app.geometry("1338x595+360+80")
    app.tk.call("tk", "scaling", 1.3)
    app.resizable(False, False)
    app.attributes("-topmost", True)
    app.mainloop()
