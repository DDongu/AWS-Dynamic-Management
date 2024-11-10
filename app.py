from flask import Flask, render_template, request, redirect, url_for
import boto3
from aws_manager import AwsManger

ec2 = boto3.client("ec2")
ssm = boto3.client("ssm")
aws_manager = AwsManger(ec2, ssm)

app = Flask(__name__)


@app.route("/instance")
def index():
    instances = aws_manager.list_instances()
    images = aws_manager.list_images()
    return render_template("index.html", instances=instances, images=images)


@app.route("/condor")
def condor():
    instances = aws_manager.list_instances()
    status = request.args.get("status")
    return render_template("condor.html", instances=instances, status=status)


@app.route("/start_instance", methods=["POST"])
def start_instance():
    instance_id = request.form["instance_id"]
    message = aws_manager.start_instance(instance_id)
    return redirect(url_for("index"))


@app.route("/stop_instance", methods=["POST"])
def stop_instance():
    instance_id = request.form["instance_id"]
    message = aws_manager.stop_instance(instance_id)
    return redirect(url_for("index"))


@app.route("/reboot_instance", methods=["POST"])
def reboot_instance():
    instance_id = request.form["instance_id"]
    message = aws_manager.reboot_instance(instance_id)
    return redirect(url_for("index"))


@app.route("/create_instance", methods=["POST"])
def create_instance():
    ami_id = request.form["ami_id"]
    message = aws_manager.create_instance(ami_id)
    return redirect(url_for("index"))


@app.route("/list_images")
def list_images():
    images = aws_manager.list_images()
    return render_template("images.html", images=images)


@app.route("/condor_status", methods=["POST"])
def condor_status():
    instance_id = request.form["instance_id"]
    status = aws_manager.condor_status(instance_id)
    instances = aws_manager.list_instances()
    return redirect(url_for("condor", instances=instances, status=status))


if __name__ == "__main__":
    app.run(debug=True)
