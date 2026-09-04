<p align="center">
  <img src="data/misc/png/throwdown-welcome-large.png" />
</p>

<p align="center">
  <img src="data/misc/screenshots/throwdown-ui.png" />
</p>

<h5 align="center">
  <em>Throwdown</em> is a fun little libadwaita/GTK4 app written in Python for<br> generating random skate trick combos with adjustable difficulty!
</h5>

---

### installation:

Simply paste this command onto your terminal:

```sh
wget -q https://github.com/yioannides/throwdown/releases/latest/download/throwdown-x86_64.flatpak &&
flatpak install --user -y ./throwdown-x86_64.flatpak &&
rm throwdown-x86_64.flatpak
```

### introduction:

Originally created as a standalone CLI app (drafted in bash / completed in Python) for getting better at skateboarding (in real life, as well as in video games like Session: Skate Sim and Skater XL). I always wanted to develop a libadwaita app, so this became the perfect challenge for me to turn it into my first GTK app as a non-programmer!

### features:

- Three levels of difficulty (easy, medium, hard) and random mode
- Type of modules: stance, direction, spin, flip, grind, lateflip & ground tricks
- Named tricks (example: `Fakie BS 360` -> `Full Cab`)

### translations:

You can create a new translation file by running run the po-generator tool with the [ISO language code](https://www.w3schools.com/TAgs/ref_language_codes.asp) of your choice, for example Swedish:

```sh
git clone https://github.com/yioannides/throwdown.git
cd throwdown/tools
./gen-po.sh sv
```

### resources (for absolute beginners):

- Built using [GNOME Builder](https://flathub.org/en/apps/org.gnome.Builder)'s Python template
- [Welcome To GNOME portal](https://welcome.gnome.org/team/programming/) for cloning and studying completed / published Python apps
- [Workbench](https://flathub.org/en/apps/re.sonny.Workbench) by Sonny Piers
- GeopJr's [GTK4 development guide](https://ultimate-gtk4-crystal-guide.geopjr.dev/) (primarily focused on the Crystal language, but offers invaluable transferable knowledge on the start-to-end process of preparing and developing a GTK4 app)
