#
# Binary Ninja Loader for Cortex-M3
#

from binaryninja import *
import struct
import traceback
import os

PLATFORM = "thumb2"
BASE_ADDR = 0x08000000
ROM_OFFSET = 0xF4

class M3View(BinaryView):
	name = "M3"
	long_name = "Cortex-M3"

	def __init__(self, data):
		BinaryView.__init__(self, parent_view = data, file_metadata = data.file)

	@classmethod
	def is_valid_for_data(self, data):
		return True		# not sure how to validate Cortex-M3 FW yet, maybe by # of addresses in table?

	def init(self):
		try:
			exception_table = self.parent_view.read(0, 232)
			# set data type to data segment offsets

			# SRAM
			#	add_auto_segment(start, length, data_offset, data_length, flags)
			self.add_auto_segment(0x20000000, 0x20000000, 0, 0, SegmentReadable | SegmentWritable | SegmentExecutable)
			# Flash Memory
			self.add_auto_segment(0x08000000, 0x1FFFF, ROM_OFFSET, 0x1FFFF, SegmentReadable | SegmentExecutable)

			self.add_entry_point("thumb2", 0x080000F4) 
			self.update_analysis()

			return True
		except:
			log_error(traceback.format_exc())
			return False

	def perform_is_executable(self):
		return True

	def perform_get_entry_point(self):
		return True

M3View.register()
