# =========================
# GPIO PINS
# =========================

LEFT_MOTOR_PIN = 17
RIGHT_MOTOR_PIN = 27
BUTTON_PIN = 22

# Button uses pull-up → LOW when pressed
BUTTON_ACTIVE_STATE = 0
SHOW_PREVIEW = False

# =========================
# MOTOR TIMINGS
# =========================

# Object pulse (short)
OBJECT_PULSE = 0.30

# Person pulse (longer so user can distinguish)
PERSON_PULSE = 0.80


# =========================
# MORSE TIMINGS
# =========================

DOT_TIME = 0.20
DASH_TIME = 0.60

SYMBOL_GAP = 0.20
LETTER_GAP = 0.60
WORD_GAP = 1.20


# =========================
# BUTTON / MORSE INPUT
# =========================

# Threshold to decide dot vs dash
MORSE_DASH_THRESHOLD = 0.35

# Pause → end of letter
LETTER_TIMEOUT = 0.90

# Pause -> end of word
WORD_TIMEOUT = 1.60

# Pause → send full message
MESSAGE_TIMEOUT = 2.80


# =========================
# MODE SWITCH (ONE BUTTON)
# =========================

# Hold to ENTER conversation mode
MODE_HOLD_TIME = 2.00

# Longer hold to EXIT conversation mode
EXIT_HOLD_TIME = 2.00


# =========================
# SPEECH SETTINGS
# =========================

# Max time for one phrase
SPEECH_PHRASE_TIME_LIMIT = 20

# Silence timeout → stop listening
SPEECH_SILENCE_TIMEOUT = 5


# =========================
# CAMERA SETTINGS
# =========================

FRAME_WIDTH = 320
FRAME_HEIGHT = 240


# =========================
# DISTANCE HEURISTICS
# =========================

# These are based on bounding box area
# (you will tune these later)

OBJECT_NEAR_AREA = 22000
OBJECT_MID_AREA = 9000

PERSON_NEAR_AREA = 28000


# =========================
# DETECTION FILTERS
# =========================

MIN_OBJECT_AREA = 2500

# HOG detector confidence threshold
PERSON_CONFIDENCE_THRESHOLD = 0.35


# =========================
# SYSTEM STATES
# =========================

STATE_OBSTACLE = "obstacle"
STATE_CONVERSATION = "conversation"


# =========================
# FALLBACKS
# =========================

# If mic fails → allow typed input
ALLOW_TYPED_SPEECH_FALLBACK = True