import os
import re
import subprocess
import sys
import argparse
import shutil

def run_command(cmd):
    print(f"Running: {' '.join(cmd)}")
    npx = shutil.which("npx")
    if npx is None:
        sys.exit("Error: npx not found on PATH")
    subprocess.run([npx] + cmd[1:], check=True)

def convert_to_standalone(html):
    """Convert sub-comp format (<template>-wrapped) to standalone format for -c rendering."""

    # Extract GSAP script src from inside <template>
    gsap_match = re.search(
        r'<script\s+src="[^"]*gsap[^"]*"[^>]*>\s*</script>',
        html
    )
    gsap_tag = gsap_match.group(0) if gsap_match else ""

    # Extract <style>...</style> from inside <template>
    style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    style_block = f"<style>{style_match.group(1)}</style>" if style_match else ""

    # Extract the root div and everything after it up to the last </script>
    root_start = re.search(r'(<div\s+id="root"[^>]*>)', html)
    if not root_start:
        raise ValueError("Could not find <div id=\"root\" in composition")

    # Find the last </script> before </template>
    template_end = html.rfind('</template>')
    last_script_end = html.rfind('</script>', 0, template_end)
    if last_script_end == -1:
        raise ValueError("Could not find timeline script in composition")

    # Find the opening <script> of the timeline block
    script_open = html.rfind('<script>', 0, last_script_end)
    if script_open == -1 or script_open < root_start.start():
        raise ValueError("Could not find timeline <script> after root div")

    # Root div content: from root div opening tag to just before the last <script>
    root_block = html[root_start.start():script_open].rstrip()

    # Timeline script: from last <script> to last </script>
    timeline_script = html[script_open:last_script_end + len('</script>')]

    # Get the meta tags from original head
    head_open = re.search(r'<head>.*?</head>', html, re.DOTALL)
    if head_open:
        original_head = head_open.group(0)
        meta_tags = '\n    '.join(re.findall(r'<meta[^>]+>', original_head))
    else:
        meta_tags = '<meta charset="UTF-8">\n    <meta name="viewport" content="width=1920, height=1080">'

    standalone = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    {meta_tags}
    {gsap_tag}
    {style_block}
  </head>
  <body>
    {root_block}
    {timeline_script}
  </body>
</html>"""

    return standalone


def render_scene(scene_name):
    if not re.fullmatch(r"[\w.-]+", scene_name):
        sys.exit(f"Invalid scene name: {scene_name}")

    # Check if file is in root folder first, then compositions folder
    if os.path.exists(f"{scene_name}.html"):
        input_path = f"{scene_name}.html"
    elif os.path.exists(f"compositions/{scene_name}.html"):
        input_path = f"compositions/{scene_name}.html"
    else:
        print(f"Error: Could not find {scene_name}.html in root or compositions/")
        sys.exit(1)

    # Read the sub-comp file
    with open(input_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Convert to standalone format
    standalone_html = convert_to_standalone(html)

    # Write to tmp/
    os.makedirs("tmp", exist_ok=True)
    tmp_path = f"tmp/{scene_name}.html"
    with open(tmp_path, 'w', encoding='utf-8') as f:
        f.write(standalone_html)

    output_path = f"renders/{scene_name}.mp4"
    os.makedirs("renders", exist_ok=True)

    cmd = [
        "npx", "--yes", "hyperframes@0.8.3",
        "render",
        "--docker",
        "-c", tmp_path,
        "--quality", "high",
        "--output", output_path
    ]

    print(f"Rendering scene: {scene_name}...")
    try:
        run_command(cmd)
        print(f"Done! Saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Render failed (exit {e.returncode})")
        sys.exit(e.returncode)
    finally:
        shutil.rmtree("tmp", ignore_errors=True)


def render_all():
    os.makedirs("renders", exist_ok=True)

    cmd = [
        "npx", "--yes", "hyperframes@0.8.3",
        "render",
        "--docker",
        "--quality", "high",
        "--output", "renders/output.mp4"
    ]
    print("Rendering all scenes...")
    run_command(cmd)
    print("Done! Saved to renders/output.mp4")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render Hyperframes scenes dynamically")
    parser.add_argument("--scene", help="Name of the scene to render (e.g., 01-ticket-inbox)")
    args = parser.parse_args()

    if args.scene:
        render_scene(args.scene)
    else:
        render_all()
