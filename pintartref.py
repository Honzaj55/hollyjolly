import os
import json
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import webbrowser
import requests
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

CONFIG_FILE = "config.json"

def get_random_image_with_selenium(url, timeout=15):
    """Render the site and fetch a random visible image + its page link."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
        time.sleep(1.0)

        images = driver.find_elements(By.TAG_NAME, "img")
        if not images:
            raise ValueError("No visible images found on page.")

        chosen = random.choice(images)
        src = chosen.get_attribute("src")
        page_url = driver.current_url

        if not src:
            raise ValueError("Image has no src attribute.")

        headers = {"User-Agent": "Mozilla/5.0", "Referer": url}
        r = requests.get(src, headers=headers, timeout=10)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content))
        return img, page_url

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch image:\n{e}")
        return None, None
    finally:
        driver.quit()

def save_config(folders, websites):
    data = {"folders": folders, "websites": websites}
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"folders": {}, "websites": {}}

def setup_window():
    setup = tk.Tk()
    setup.title("ArtRef Setup")

    folder_entries = []
    web_entries = []

    # ---------- Folder section ----------
    tk.Label(setup, text="Folders").pack()
    def add_folder_field(name="", path=""):
        frame = tk.Frame(setup)
        frame.pack(pady=2)
        name_entry = tk.Entry(frame, width=20)
        name_entry.insert(0, name)
        name_entry.pack(side="left", padx=5)
        path_entry = tk.Entry(frame, width=40)
        path_entry.insert(0, path)
        path_entry.pack(side="left", padx=5)
        def browse_folder():
            folder = filedialog.askdirectory()
            if folder:
                path_entry.delete(0, tk.END)
                path_entry.insert(0, folder)
        browse_btn = tk.Button(frame, text="Browse", command=browse_folder)
        browse_btn.pack(side="left", padx=5)
        folder_entries.append((name_entry, path_entry))
    tk.Button(setup, text="Add Folder", command=lambda: add_folder_field()).pack(pady=3)

    # ---------- Website section ----------
    tk.Label(setup, text="Websites").pack(pady=5)
    def add_web_field(name="", url=""):
        frame = tk.Frame(setup)
        frame.pack(pady=2)
        name_entry = tk.Entry(frame, width=20)
        name_entry.insert(0, name)
        name_entry.pack(side="left", padx=5)
        url_entry = tk.Entry(frame, width=50)
        url_entry.insert(0, url)
        url_entry.pack(side="left", padx=5)
        web_entries.append((name_entry, url_entry))
    tk.Button(setup, text="Add Website", command=lambda: add_web_field()).pack(pady=3)

    # ---------- Save ----------
    def save_and_start():
        folders = {}
        websites = {}
        for name_entry, path_entry in folder_entries:
            name, path = name_entry.get().strip(), path_entry.get().strip()
            if name and path:
                folders[name] = path
        for name_entry, url_entry in web_entries:
            name, url = name_entry.get().strip(), url_entry.get().strip()
            if name and url:
                websites[name] = url
        if not folders and not websites:
            messagebox.showerror("Error", "Please add at least one folder or website.")
            return
        save_config(folders, websites)
        setup.destroy()
        start_main_window(folders, websites)

    tk.Button(setup, text="Save & Start", command=save_and_start).pack(pady=10)
    setup.mainloop()

def start_main_window(folders, websites):
    window = tk.Tk()
    window.title("ArtRef")
    displayed_labels = {}
    displayed_images = []

    def image(category):
        nonlocal displayed_images, displayed_labels

        # Clear previous images
        for widget in window.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Frame):
                widget.destroy()

        displayed_images.clear()
        displayed_labels.clear()

        if category == "All":
            sources = list(folders.items()) + list(websites.items())
            if not sources:
                messagebox.showerror("Error", "No folders or websites configured.")
                return

            selected = random.sample(sources, k=min(4, len(sources)))

            for name, source in selected:
                if name in folders:
                    path = source
                    if not os.path.isdir(path):
                        continue
                    files = os.listdir(path)
                    if not files:
                        continue
                    choice = random.choice(files)
                    img = Image.open(os.path.join(path, choice))
                    img = img.resize((500, 700))
                    photo = ImageTk.PhotoImage(img)
                    label = tk.Label(window, image=photo)
                    label.pack(side="left", fill="y", padx=5)
                    displayed_images.append(photo)

                elif name in websites:
                    url = source
                    img, page_link = get_random_image_with_selenium(url)
                    if img:
                        display = img.copy()
                        display.thumbnail((800, 1000), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(display)

                        frame = tk.Frame(window)
                        frame.pack(side="left", fill="y", padx=5)

                        label = tk.Label(frame, image=photo)
                        label.pack()

                        def open_source(u=page_link):
                            if u:
                                webbrowser.open(u)

                        open_btn = tk.Button(frame, text=f"Open {name}", command=open_source)
                        open_btn.pack(pady=4)

                        displayed_images.append(photo)

        elif category in folders:
            path = folders[category]
            if not os.path.isdir(path):
                messagebox.showerror("Error", f"Folder '{category}' does not exist.")
                return
            files = os.listdir(path)
            if not files:
                messagebox.showerror("Error", f"No images found in folder '{category}'.")
                return
            choice = random.choice(files)
            img = Image.open(os.path.join(path, choice))
            img = img.resize((500, 700))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(window, image=photo)
            label.pack(side="left", fill="y")
            displayed_images.append(photo)
            displayed_labels[category] = label

        elif category in websites:
            url = websites[category]
            img, page_link = get_random_image_with_selenium(url)
            if img:
                display = img.copy()
                display.thumbnail((800, 1000), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(display)

                frame = tk.Frame(window)
                frame.pack(side="left", fill="y", padx=5)

                label = tk.Label(frame, image=photo)
                label.pack()

                def open_source(u=page_link):
                    if u:
                        webbrowser.open(u)

                open_btn = tk.Button(frame, text="Open page", command=open_source)
                open_btn.pack(pady=4)

                displayed_images.append(photo)
                displayed_labels[category] = frame

    # Buttons for each folder
    for name in folders.keys():
        tk.Button(window, text=name, width=20, command=lambda n=name: image(n)).pack()
    # Buttons for each website
    for name in websites.keys():
        tk.Button(window, text=f"{name} (web)", width=20, command=lambda n=name: image(n)).pack()
    # All button
    tk.Button(window, text="All", width=20, command=lambda: image("All")).pack(pady=5)
    # Settings button
    tk.Button(window, text="Settings", width=20, command=lambda: (window.destroy(), setup_window())).pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    data = load_config()
    folders, websites = data.get("folders", {}), data.get("websites", {})
    if folders or websites:
        start_main_window(folders, websites)
    else:
        setup_window()
