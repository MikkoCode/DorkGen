import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from base64 import b64decode
import requests
import asyncio
import threading
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup

from dork_generation import create_dorks
from ui_setup import setup_ui

# Read the API key from a file
API_KEY_FILE = 'zyte_api_key.txt'


def read_api_key():
    try:
        with open(API_KEY_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ''


def save_api_key(api_key):
    with open(API_KEY_FILE, 'w') as file:
        file.write(api_key)


ZYTE_API_KEY = read_api_key()
title = "DorkGen"
version = 0.10


class DorkGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{title} v{version}")  # Set window title

        self.api_key_var = tk.StringVar(value=ZYTE_API_KEY)
        self.entry = tk.Entry(self.root)
        self.generate_button = tk.Button(self.root)
        self.run_button = tk.Button(self.root)
        self.pause_button = tk.Button(self.root)
        self.progress = ttk.Progressbar(self.root)
        self.dorks_text = tk.Text(self.root, selectbackground='#5a5a5a', selectforeground='white')
        self.dorks_label = tk.Label(self.root)
        self.results_text = tk.Text(self.root, selectbackground='#5a5a5a', selectforeground='white')
        self.results_label = tk.Label(self.root)
        self.log_text = tk.Text(self.root)
        self.filter_entry = tk.Entry(self.root)
        self.filter_button = tk.Button(self.root)

        self.dorks = []
        self.filtered_dorks = []
        self.searching = False
        self.paused_index = 0
        self.filter_criteria = ''
        self.setup_ui()
        self.apply_dark_mode()  # Apply dark mode

    def setup_ui(self):
        setup_ui(self)

    def apply_dark_mode(self):
        self.root.configure(bg='#1e1e1e')
        self.entry.configure(bg='#3a3a3a', fg='white')
        self.generate_button.configure(bg='#3a3a3a', fg='white')
        self.run_button.configure(bg='#3a3a3a', fg='white')
        self.pause_button.configure(bg='#3a3a3a', fg='white')
        self.dorks_text.configure(bg='#3a3a3a', fg='white')
        self.dorks_label.configure(bg='#1e1e1e', fg='white')
        self.results_text.configure(bg='#3a3a3a', fg='white')
        self.results_label.configure(bg='#1e1e1e', fg='white')
        self.log_text.configure(bg='#3a3a3a', fg='white')
        self.filter_entry.configure(bg='#3a3a3a', fg='white')
        self.filter_button.configure(bg='#3a3a3a', fg='white')

    def log(self, message, level='info'):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color = {'info': 'lightgrey', 'warning': 'yellow', 'error': 'red'}[level]
        self.log_text.insert(tk.END, f"{timestamp} - {message}\n", level)
        self.log_text.tag_config(level, foreground=color)
        self.log_text.see(tk.END)

    def update_dorks_label(self):
        num_dorks = int(self.dorks_text.index('end-1c').split('.')[0]) - 1
        self.dorks_label.config(text=f"Dorks ({num_dorks})")

    def update_results_label(self):
        num_results = int(self.results_text.index('end-1c').split('.')[0]) - 1
        self.results_label.config(text=f"Search Results ({num_results})")

    def generate_dorks(self):
        self.log("Starting Dork generation...", 'info')
        self.run_button.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.run_asyncio_task, args=(self.generate_dorks_async,))
        thread.start()

    def run_asyncio_task(self, coro):
        asyncio.run(coro())

    async def generate_dorks_async(self):
        site_url = self.entry.get()
        if not site_url:
            messagebox.showerror("Input Error", "Please enter a site URL.")
            return

        html_source = await self.fetch_html_source(site_url)
        if not html_source:
            messagebox.showerror("Fetch Error", "Could not fetch HTML source.")
            return

        self.dorks = create_dorks(html_source)
        self.filtered_dorks = self.dorks[:]
        self.dorks_text.delete("1.0", tk.END)
        self.dorks_text.insert(tk.END, "\n".join(self.dorks) + "\n")
        self.update_dorks_label()
        self.run_button.config(state=tk.NORMAL, text="Run Search")
        self.log("Dork generation completed.", 'info')

    def run_search(self):
        self.log("Starting search...", 'info')
        self.searching = True
        self.pause_button.config(state=tk.NORMAL, text="Pause")
        self.run_button.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.run_asyncio_task, args=(self.search_dorks_async,))
        thread.start()

    def pause_search(self):
        self.log("Pausing search...", 'warning')
        self.searching = False
        self.run_button.config(state=tk.NORMAL, text="Continue Search")
        self.pause_button.config(state=tk.DISABLED)

    async def fetch_html_source(self, url):
        try:
            self.log(f"Fetching HTML source for: {url}", 'info')
            api_response = requests.post(
                "https://api.zyte.com/v1/extract",
                auth=(self.api_key_var.get(), ""),
                json={"url": url, "httpResponseBody": True},
            )
            api_response.raise_for_status()
            http_response_body = b64decode(api_response.json()["httpResponseBody"])
            self.log("HTML source fetched successfully.", 'info')
            return http_response_body.decode('utf-8')
        except requests.RequestException as e:
            self.log(f"Error fetching HTML source: {e}", 'error')
            return None

    async def search_dorks_async(self):
        total_dorks = len(self.filtered_dorks)
        self.progress["maximum"] = total_dorks
        for index in range(self.paused_index, total_dorks):
            if not self.searching:
                self.paused_index = index
                self.log("Search paused by user.", 'warning')
                break
            dork = self.filtered_dorks[index]
            try:
                search_results = await self.search_google_with_zyte(dork)
                self.display_results(search_results)
            except Exception as e:
                self.log(f"API Error: {str(e)}", 'error')
            self.progress["value"] = index + 1
        else:
            self.paused_index = 0
            self.log("Search completed.", 'info')
        self.pause_button.config(state=tk.DISABLED)
        self.run_button.config(state=tk.NORMAL, text="Run Search")

    async def search_google_with_zyte(self, dork):
        google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(dork)}"
        try:
            self.log(f"Searching Google with dork: {dork}", 'info')
            api_response = requests.post(
                "https://api.zyte.com/v1/extract",
                auth=(self.api_key_var.get(), ""),
                json={"url": google_search_url, "httpResponseBody": True},
            )
            api_response.raise_for_status()
            http_response_body = b64decode(api_response.json()["httpResponseBody"])
            self.log("Google search completed.", 'info')
            return self.extract_search_results(http_response_body.decode('utf-8'))
        except requests.RequestException as e:
            self.log(f"Error searching Google: {e}", 'error')
            return []

    def extract_search_results(self, html):
        self.log("Extracting search results...", 'info')
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for g in soup.find_all(class_='g'):
            link = g.find('a', href=True)
            if link:
                results.append(link['href'])
        self.log("Search results extracted successfully.", 'info')
        return results

    def display_results(self, results):
        for result in results:
            self.results_text.insert(tk.END, f"{result}\n")
        self.results_text.see(tk.END)  # Ensure the scrollbar stays at the bottom
        self.update_results_label()
        self.log("Results displayed.", 'info')

    def save_dorks_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.dorks_text.get("1.0", tk.END))
            self.log(f"Dorks saved to {file_path}", 'info')

    def save_results_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.results_text.get("1.0", tk.END))
            self.log(f"Search results saved to {file_path}", 'info')

    def remove_dorks_duplicates(self):
        original_dorks = self.dorks_text.get("1.0", tk.END).splitlines()
        unique_dorks = list(set(filter(None, original_dorks)))  # Filter out empty lines
        duplicates_removed = len(original_dorks) - len(unique_dorks)
        self.dorks_text.delete("1.0", tk.END)
        self.dorks_text.insert(tk.END, "\n".join(unique_dorks))
        self.update_dorks_label()
        self.log(f"Removed {duplicates_removed} duplicate dorks.", 'info')

    def remove_results_duplicates(self):
        original_results = self.results_text.get("1.0", tk.END).splitlines()
        unique_results = list(set(filter(None, original_results)))  # Filter out empty lines
        duplicates_removed = len(original_results) - len(unique_results)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, "\n".join(unique_results))
        self.update_results_label()
        self.log(f"Removed {duplicates_removed} duplicate results.", 'info')

    def cleanup_dorks(self):
        original_dorks = self.dorks_text.get("1.0", tk.END).splitlines()
        cleaned_dorks = [dork for dork in original_dorks if len(dork.split('"')[1]) >= 4 and dork.strip()]
        lines_removed = len(original_dorks) - len(cleaned_dorks)
        self.dorks_text.delete("1.0", tk.END)
        self.dorks_text.insert(tk.END, "\n".join(cleaned_dorks))
        self.update_dorks_label()
        self.log(f"Removed {lines_removed} invalid dorks.", 'info')

    def save_api_key(self):
        new_api_key = self.api_key_var.get()
        save_api_key(new_api_key)
        self.log("API key saved.", 'info')

    def apply_filter(self):
        filter_text = self.filter_entry.get().strip()
        if not filter_text:
            messagebox.showerror("Input Error", "Please enter filter criteria.")
            return

        self.filtered_dorks = [dork for dork in self.dorks if filter_text in dork]
        self.dorks_text.delete("1.0", tk.END)
        self.dorks_text.insert(tk.END, "\n".join(self.filtered_dorks) + "\n")
        self.update_dorks_label()
        self.log(f"Applied filter: {filter_text}. {len(self.filtered_dorks)} dorks match the criteria.", 'info')

    def remove_filter(self):
        self.filtered_dorks = self.dorks[:]
        self.dorks_text.delete("1.0", tk.END)
        self.dorks_text.insert(tk.END, "\n".join(self.filtered_dorks) + "\n")
        self.update_dorks_label()
        self.log("Filter removed. Showing all dorks.", 'info')

    def remove_selected_dorks(self):
        try:
            selected_indices = self.dorks_text.tag_ranges(tk.SEL)
            if not selected_indices:
                messagebox.showerror("Selection Error", "Please select one or more lines to remove.")
                return
            selected_lines = [int(self.dorks_text.index(index).split('.')[0]) for index in selected_indices]
            remaining_dorks = [line for i, line in enumerate(self.filtered_dorks) if i + 1 not in selected_lines]
            self.filtered_dorks = remaining_dorks
            self.dorks_text.delete("1.0", tk.END)
            self.dorks_text.insert(tk.END, "\n".join(self.filtered_dorks) + "\n")
            self.update_dorks_label()
            self.log(f"Removed {len(selected_lines)} selected dorks.", 'info')
        except Exception as e:
            self.log(f"Error removing selected dorks: {e}", 'error')

    def remove_selected_results(self):
        try:
            selected_indices = self.results_text.tag_ranges(tk.SEL)
            if not selected_indices:
                messagebox.showerror("Selection Error", "Please select one or more lines to remove.")
                return
            selected_lines = [int(self.results_text.index(index).split('.')[0]) for index in selected_indices]
            remaining_results = [line for i, line in enumerate(self.results_text.get("1.0", tk.END).splitlines()) if
                                 i + 1 not in selected_lines]
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(tk.END, "\n".join(remaining_results) + "\n")
            self.update_results_label()
            self.log(f"Removed {len(selected_lines)} selected results.", 'info')
        except Exception as e:
            self.log(f"Error removing selected results: {e}", 'error')
