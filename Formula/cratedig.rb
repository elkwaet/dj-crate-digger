class Cratedig < Formula
  desc "Outil TUI d'extraction et de structuration de tracklists YouTube pour DJs"
  homepage "https://github.com/elkwaet/dj-crate-digger"
  url "https://github.com/elkwaet/dj-crate-digger/archive/refs/tags/v1.1.0.tar.gz"
  sha256 "REPLACE_WITH_SHA256"
  license "MIT"

  depends_on "python@3.12"

  def install
    python3 = Formula["python@3.12"].opt_bin/"python3.12"
    venv = libexec/"venv"

    system python3, "-m", "venv", "--without-pip", venv
    system venv/"bin/python3", "-m", "ensurepip"
    system venv/"bin/python3", "-m", "pip", "install", "--quiet", "--upgrade", "pip"
    system venv/"bin/pip", "install", "--quiet", "yt-dlp", "rich", "typer", "questionary"

    # Installation du code source
    libexec.install Dir["src/*"]

    # Création du wrapper global dans bin/cratedig
    (bin/"cratedig").write <<~SH
      #!/bin/bash
      exec "#{venv}/bin/python3" "#{libexec}/cli.py" "$@"
    SH
    chmod 0755, bin/"cratedig"
  end

  def caveats
    <<~EOS
      DJ Crate Digger est maintenant installé !
      Tu peux lancer l'outil avec la commande :
        cratedig
    EOS
  end

  test do
    # Simple vérification que l'application démarre
    system "#{bin}/cratedig", "version"
  end
end
