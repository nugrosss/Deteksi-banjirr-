import tkinter as tk
import configparser

class ScaleApp:
    def __init__(self, root):
        self.root = root
        self.config = configparser.ConfigParser()
        self.config_file = 'settings.ini'
        
        self.load_settings()

        # Buat skala untuk nilai Hue
        self.hue_low_scale = tk.Scale(root, from_=0, to=180, label='Lower Hue', orient='horizontal')
        self.hue_high_scale = tk.Scale(root, from_=0, to=180, label='Upper Hue', orient='horizontal')

        # Buat skala untuk nilai Saturation
        self.saturation_low_scale = tk.Scale(root, from_=0, to=255, label='Lower Saturation', orient='horizontal')
        self.saturation_high_scale = tk.Scale(root, from_=0, to=255, label='Upper Saturation', orient='horizontal')

        # Buat skala untuk nilai Value
        self.value_low_scale = tk.Scale(root, from_=0, to=255, label='Lower Value', orient='horizontal')
        self.value_high_scale = tk.Scale(root, from_=0, to=255, label='Upper Value', orient='horizontal')

        # Atur nilai awal skala dari pengaturan yang disimpan
        self.hue_low_scale.set(self.config.getint('settings', 'lower_hue', fallback=0))
        self.hue_high_scale.set(self.config.getint('settings', 'upper_hue', fallback=180))
        self.saturation_low_scale.set(self.config.getint('settings', 'lower_sat', fallback=0))
        self.saturation_high_scale.set(self.config.getint('settings', 'upper_sat', fallback=255))
        self.value_low_scale.set(self.config.getint('settings', 'lower_val', fallback=0))
        self.value_high_scale.set(self.config.getint('settings', 'upper_val', fallback=255))

        # Tambahkan skala ke GUI
        self.hue_low_scale.pack()
        self.hue_high_scale.pack()
        self.saturation_low_scale.pack()
        self.saturation_high_scale.pack()
        self.value_low_scale.pack()
        self.value_high_scale.pack()

        # Tambahkan event listener untuk menyimpan pengaturan saat skala diubah
        self.hue_low_scale.bind("<Motion>", self.save_settings)
        self.hue_high_scale.bind("<Motion>", self.save_settings)
        self.saturation_low_scale.bind("<Motion>", self.save_settings)
        self.saturation_high_scale.bind("<Motion>", self.save_settings)
        self.value_low_scale.bind("<Motion>", self.save_settings)
        self.value_high_scale.bind("<Motion>", self.save_settings)

    def load_settings(self):
        """Load settings from a configuration file."""
        self.config.read(self.config_file)

    def save_settings(self, event):
        """Save the current settings to a configuration file."""
        self.config['settings'] = {
            'lower_hue': self.hue_low_scale.get(),
            'upper_hue': self.hue_high_scale.get(),
            'lower_sat': self.saturation_low_scale.get(),
            'upper_sat': self.saturation_high_scale.get(),
            'lower_val': self.value_low_scale.get(),
            'upper_val': self.value_high_scale.get()
        }
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScaleApp(root)
    root.mainloop()
