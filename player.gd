extends Node2D

var speed := 200
var velocity := Vector2.ZERO

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
@onready var interactable_shape: CollisionShape2D = $interactable_shape
@onready var collision_shape_2d: CollisionShape2D = $CollisionShape2D
@onready var wallet_amount: Label = $BoxContainer/wallet_amount
@export var wallet_amount_value: PackedScene
func _process(delta: float) -> void:
	velocity = Vector2.ZERO


	if Input.is_action_pressed("move_right"):
		velocity.x += 1
	if Input.is_action_pressed("move_left"):
		velocity.x -= 1
	if Input.is_action_pressed("move_down"):
		velocity.y += 1
	if Input.is_action_pressed("move_up"):
		velocity.y -= 1


	if velocity == Vector2.ZERO:
		animated_sprite_2d.play("move_down") # Idle animation
	else:
		if abs(velocity.x) > abs(velocity.y):
			if velocity.x > 0:
				animated_sprite_2d.play("move_right")
			else:
				animated_sprite_2d.play("move_left")
		else:
			if velocity.y > 0:
				animated_sprite_2d.play("move_down")
			else:
				animated_sprite_2d.play("move_up")

	position += velocity.normalized() * speed * delta

function display_wallet_amount():
	var wallet_instance = wallet_amount_value.instantiate()
	wallet_instance.text = str(get_wallet_amount())

