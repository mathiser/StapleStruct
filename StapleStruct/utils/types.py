from typing import NewType, Dict, List
import SimpleITK as sitk

LabelPaths = NewType("LabelPaths", Dict[str, List[str]])
LabelImages = NewType("LabelImages", Dict[str, List[sitk.Image]])
