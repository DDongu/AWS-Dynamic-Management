from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import boto3
import secrets
from aws_manager import AwsManger

ec2 = boto3.client("ec2")
ssm = boto3.client("ssm")
cloudwatch = boto3.client("cloudwatch")
aws_manager = AwsManger(ec2, ssm, cloudwatch)

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)


@app.route("/")
def index():
    return redirect(url_for("instance"))


@app.route("/instance")
def instance():
    instances = aws_manager.list_instances()
    images = aws_manager.list_images()
    return render_template("instance.html", instances=instances, images=images)


@app.route("/condor")
def condor():
    instances = aws_manager.list_instances()
    return render_template("condor.html", instances=instances)


@app.route("/zone")
def list_available_zones():
    zones = aws_manager.list_available_zones()
    regions = aws_manager.list_available_regions()
    return render_template("zones.html", zones=zones, regions=regions)


@app.route("/dashboard")
def dashboard():
    instances = aws_manager.list_instances()
    return render_template("dashboard.html", instances=instances)


@app.route("/start_instance", methods=["POST"])
def start_instance():
    instance_id = request.form["instance_id"]
    message = aws_manager.start_instance(instance_id)
    flash(message)
    return redirect(url_for("instance"))


@app.route("/stop_instance", methods=["POST"])
def stop_instance():
    instance_id = request.form["instance_id"]
    message = aws_manager.stop_instance(instance_id)
    flash(message)
    return redirect(url_for("instance"))


@app.route("/terminate_instance", methods=["POST"])
def terminate_instance():
    instance_id = request.form["instance_id"]
    message = aws_manager.terminate_instance(instance_id)
    flash(message)
    return redirect(url_for("instance"))


@app.route("/reboot_instance", methods=["POST"])
def reboot_instance():
    instance_id = request.form["instance_id"]
    message = aws_manager.reboot_instance(instance_id)
    flash(message)
    return redirect(url_for("instance"))


@app.route("/create_instance", methods=["POST"])
def create_instance():
    ami_id = request.form["ami_id"]
    instance_name = request.form["instance_name"]
    message = aws_manager.create_instance(ami_id, instance_name)
    flash(message)
    return redirect(url_for("instance"))


@app.route("/list_images")
def list_images():
    images = aws_manager.list_images()
    return render_template("images.html", images=images)


@app.route("/condor_status", methods=["POST"])
def condor_status():
    instance_id = request.form["instance_id"]
    status = aws_manager.condor_status(instance_id)
    flash({"status": status, "instance_id": instance_id})
    return redirect(url_for("condor"))


@app.route("/get_metrics", methods=["POST"])
def get_metrics():
    instance_id = request.form["instance_id"]
    metrics = aws_manager.get_metrics_statistics(instance_id)
    cpu_data = metrics[0]["Datapoints"]
    networkin_data = metrics[1]["Datapoints"]
    networkout_data = metrics[2]["Datapoints"]
    print(cpu_data)
    return jsonify(
        {
            "cpu_data": cpu_data,
            "networkin_data": networkin_data,
            "networkout_data": networkout_data,
        }
    )

@app.route("/add_tags", methods=["POST"])
def add_tags():
    instance_id = request.form["instance_id"]
    tag_key = request.form["tag_key"]
    tag_value = request.form["tag_value"]
    
    tags = {tag_key: tag_value}  # 입력받은 태그 정보를 딕셔너리로 구성
    message = aws_manager.add_tags(instance_id, tags)
    flash(message)
    return redirect(url_for("instance"))

if __name__ == "__main__":
    app.run(debug=True)
