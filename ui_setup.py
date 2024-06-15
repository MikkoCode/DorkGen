import tkinter as tk
from tkinter import ttk


def setup_ui(app):
    main_frame = tk.Frame(app.root)
    main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    setup_url_frame(app, main_frame)
    setup_control_frame(app, main_frame)
    setup_filter_frame(app, main_frame)
    setup_dorks_frame(app, main_frame)
    setup_results_frame(app, main_frame)
    setup_log_frame(app, main_frame)
    setup_api_key_frame(app, main_frame)  # Added this line


def setup_url_frame(app, parent):
    url_frame = tk.Frame(parent, bg='#2e2e2e')
    url_frame.pack(fill=tk.X, pady=5)

    app.label = tk.Label(url_frame, text="Enter Site URL:", bg='#2e2e2e', fg='white')
    app.label.pack(side=tk.LEFT, padx=5)

    app.entry = tk.Entry(url_frame, width=50, bg='#444444', fg='white')
    app.entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    app.generate_button = tk.Button(url_frame, text="Generate Dorks", command=app.generate_dorks, bg='#444444', fg='white')
    app.generate_button.pack(side=tk.LEFT, padx=5)


def setup_control_frame(app, parent):
    control_frame = tk.Frame(parent, bg='#2e2e2e')
    control_frame.pack(fill=tk.X, pady=5)

    app.run_button = tk.Button(control_frame, text="Run Search", command=app.run_search, state=tk.DISABLED, bg='#444444', fg='white')
    app.run_button.pack(side=tk.LEFT, padx=5)

    app.pause_button = tk.Button(control_frame, text="Pause", command=app.pause_search, state=tk.DISABLED, bg='#444444', fg='white')
    app.pause_button.pack(side=tk.LEFT, padx=5)

    app.progress = ttk.Progressbar(control_frame, orient="horizontal", length=300, mode="determinate")
    app.progress.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)


def setup_filter_frame(app, parent):
    filter_frame = tk.Frame(parent, bg='#2e2e2e')
    filter_frame.pack(fill=tk.X, pady=5)

    app.filter_label = tk.Label(filter_frame, text="Filter Dorks:", bg='#2e2e2e', fg='white')
    app.filter_label.pack(side=tk.LEFT, padx=5)

    app.filter_entry = tk.Entry(filter_frame, width=30, bg='#444444', fg='white')
    app.filter_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    app.filter_button = tk.Button(filter_frame, text="Apply Filter", command=app.apply_filter, bg='#444444', fg='white')
    app.filter_button.pack(side=tk.LEFT, padx=5)


def setup_dorks_frame(app, parent):
    dorks_frame = tk.Frame(parent, bg='#2e2e2e')
    dorks_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    app.dorks_label = tk.Label(dorks_frame, text="Dorks (0)", bg='#2e2e2e', fg='white')
    app.dorks_label.pack(anchor="w", padx=5)

    app.dorks_text = tk.Text(dorks_frame, height=10, width=80, bg='#444444', fg='white')
    app.dorks_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    app.dorks_scrollbar = tk.Scrollbar(dorks_frame, command=app.dorks_text.yview)
    app.dorks_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    app.dorks_text.config(yscrollcommand=app.dorks_scrollbar.set)

    dorks_button_frame = tk.Frame(dorks_frame, bg='#2e2e2e')
    dorks_button_frame.pack(side=tk.LEFT, pady=5)

    app.save_dorks_button = tk.Button(dorks_button_frame, text="Save to File", command=app.save_dorks_to_file, bg='#444444', fg='white')
    app.save_dorks_button.pack(fill=tk.X, pady=2)

    app.remove_dorks_duplicates_button = tk.Button(dorks_button_frame, text="Remove Duplicates", command=app.remove_dorks_duplicates, bg='#444444', fg='white')
    app.remove_dorks_duplicates_button.pack(fill=tk.X, pady=2)

    app.cleanup_dorks_button = tk.Button(dorks_button_frame, text="Cleanup", command=app.cleanup_dorks, bg='#444444', fg='white')
    app.cleanup_dorks_button.pack(fill=tk.X, pady=2)


def setup_results_frame(app, parent):
    results_frame = tk.Frame(parent, bg='#2e2e2e')
    results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    app.results_label = tk.Label(results_frame, text="Search Results (0)", bg='#2e2e2e', fg='white')
    app.results_label.pack(anchor="w", padx=5)

    app.results_text = tk.Text(results_frame, height=10, width=80, bg='#444444', fg='white')
    app.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    app.results_scrollbar = tk.Scrollbar(results_frame, command=app.results_text.yview)
    app.results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    app.results_text.config(yscrollcommand=app.results_scrollbar.set)

    results_button_frame = tk.Frame(results_frame, bg='#2e2e2e')
    results_button_frame.pack(side=tk.LEFT, pady=5)

    app.save_results_button = tk.Button(results_button_frame, text="Save to File", command=app.save_results_to_file, bg='#444444', fg='white')
    app.save_results_button.pack(fill=tk.X, pady=2)

    app.remove_results_duplicates_button = tk.Button(results_button_frame, text="Remove Duplicates", command=app.remove_results_duplicates, bg='#444444', fg='white')
    app.remove_results_duplicates_button.pack(fill=tk.X, pady=2)


def setup_log_frame(app, parent):
    log_frame = tk.Frame(parent, bg='#2e2e2e')
    log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    log_label = tk.Label(log_frame, text="Log", bg='#2e2e2e', fg='white')
    log_label.pack(anchor="w", padx=5)

    app.log_text = tk.Text(log_frame, height=10, width=80, bg='#444444', fg='white')
    app.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    app.log_scrollbar = tk.Scrollbar(log_frame, command=app.log_text.yview)
    app.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    app.log_text.config(yscrollcommand=app.log_scrollbar.set)


def setup_api_key_frame(app, parent):  # Add this function
    api_key_frame = tk.Frame(parent, bg='#2e2e2e')
    api_key_frame.pack(fill=tk.X, pady=5)

    api_key_label = tk.Label(api_key_frame, text="Zyte API Key:", bg='#2e2e2e', fg='white')
    api_key_label.pack(side=tk.LEFT, padx=5)

    api_key_entry = tk.Entry(api_key_frame, textvariable=app.api_key_var, width=50, bg='#444444', fg='white')
    api_key_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    save_api_key_button = tk.Button(api_key_frame, text="Save API Key", command=app.save_api_key, bg='#444444', fg='white')
    save_api_key_button.pack(side=tk.LEFT, padx=5)
