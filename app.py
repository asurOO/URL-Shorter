from flask import Flask, request, redirect
import os, sqlite3
from urllib.parse import urlparse