# DISCLAIMER!!!
**Do not use this repository if you have critical bashrc and bash aliases commands.** This project is specifically intended as a convenience tool for casual bash users. Please proceed with caution.

# About
This is project is aimed at Ubuntu 16.04 users who often use bash, terminator, Atom and Anaconda.

Its intention is to quickly deploy the same bash experience on any system. If you use this tool you will no longer edit or update the `~/.bashrc` or `~/.bash_aliases` directly. Instead you will make changes to `~/projects/autobash/bashrc_append` and `~/projects/autobash/aliases`. The changes you make here can be committed to git and when you move to a new system, you can git clone & pull and all your personal settings will be imported.

Current Version: 0.2.0 (no version control yet)


Autobash does the following:
1. Auto appends the ~/.bashrc to make the bash prompt look a little more practical with support for GIT and Anaconda
1. Auto creates aliases for easy project access with terminator and Atom.
1. Auto creates aliases and bashrc files for use with Anaconda environments.
1. Auto creates aliases for quick download of tools and added them to local path.
  - [protemplates - python & go project creator](https://github.com/ansrivas/protemplates)
  - [rmate](https://github.com/textmate/rmate)
1. Auto creates [terminator](https://launchpad.net/~gnome-terminator/+archive/ubuntu/nightly-gtk3) profiles for each project.
1. Auto creates [fzf](https://github.com/junegunn/fzf) support with which you can even quick look up [fzf_snippets](https://gist.github.com/nitred/84e11ef8b96454d39e9639ab82d9058a#file-fzf_snippets) with Alt+E shortcut.

# Dependencies
* Install [terminator gtk3](https://launchpad.net/~gnome-terminator/+archive/ubuntu/nightly-gtk3)

```
sudo add-apt-repository ppa:gnome-terminator/nightly-gtk3
sudo apt-get update
sudo apt-get install terminator
```

* Install [Atom](https://atom.io/) by downloading it from their website

* Install [Anaconda](https://www.anaconda.com/download/) by downloading it from their website and make sure to install it in the following path `~/anaconda3/` and don't append the `~/anaconda3/bin` path to the `~/.bashrc`.

# How To - First Time

### Step 1: Take a backup of `~/.bashrc` and `~/.bash_aliases` and `~/.bash_profile`
Autobash overwrites `~/.bashrc` and `~/.bash_aliases` and `~/.bash_profile` files, therefore it is **HIGHLY RECOMMENDED (mandatory even)** to take a backup of these files. If anything were to go wrong just restore the backup files and you should be as good as before.

```
cp ~/.bashrc ~/.bashrc.bak && \
cp ~/.bash_aliases ~/.bash_aliases.bak && \
cp ~/.bash_profile ~/.bash_profile.bak && \
```

### Step 2: Create a projects folder
It is highly recommended that you put all your `projects` in one single folder on your file system. For example `/home/user/projects/`.

**Example project paths**
- project "foo" location: `/home/user/projects/foo`
- project "bar" location: `/home/user/projects/bar`


### Step 3: Clone the repository
Clone the repository into the projects folder. For illustration, we will assume `/home/user/projects/` is the projects folder such that we end up with `/home/user/projects/autobash`

```
git clone https://github.com/nitred/autobash.git
cd autobash
```


### Step 4: Add custom bashrc commands to `autobash/bashrc_append`
The `~/.bashrc` file is recreated by Autobash by merging the default bashrc skeleton from `/etc/skel/.bashrc` with `autobash/bashrc_append`. Therefore you must add your custom bashrc commands to `autobash/bashrc_append`.

It is recommended that you add your custom bashrc under the user section which is demarcated.
```
############ AUTOBASH - USER SECTION ################
<add your custom bashrc commands here>
################# AUTOBASH - END ####################
```

Feel free to change the default section of the `autobash/bashrc_append` provided you know what you're doing. The default section is demarcated as follows:  
`##################### AUTOBASH ######################`


### Step 5: Add custom aliases to `autobash/aliases`
The `~/.bash_aliases` file is recreated by Autobash by merging `autobash/aliases` with an auto generated list of project aliases.Therefore you must add your custom aliases to `autobash/aliases`.


### Step 6: Add project names to `autobash/projects`
Add the name of your project to the `PROJECTS` variable. The name that you add here must be same as the name of the directory of the project.

NOTE: The `PROJECTS` variable should already contain a default project called `autobash` which should not be edited.
```
PROJECTS=(
"autobash              ;aliases;no_anaconda"
"foo                   ;aliases;no_anaconda"
"bar                   ;aliases;no_anaconda"
)
```

* TODO: Anaconda aliases
* TODO: Project aliases
* TODO: Project conda aliases


### Step 7: Run the script
Run the script by running the following:
```
cd autobash
source cp_autobash
```


# How To After First Time

* Perform Step 4 to change the custom bashrc
* Perform Step 5 to change the custom aliases
* Perform Step 6 to add a new project
* After the first time, an `alias` is generated such that it can be called from anywhere to update Autobash. Just run the following from anywhere.  
```
cp-autobash
```


# What aliases have been added?
Just have a look at your `~/.bash_aliases` to check all the aliases that have been auto generated along with the custom aliases.
