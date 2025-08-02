"""
Comprehensive Surgical Backtable Tools Database
Organized by surgical specialties with detailed instrument requirements
"""

SURGICAL_PROCEDURES = {
    # 🧠 Neurosurgery
    "Craniotomy for Tumor Resection": {
        "category": "Neurosurgery",
        "specialty": "🧠 Neurosurgery",
        "instruments": [
            "Mayfield head holder and pins",
            "Craniotome with perforator and footplate",
            "Bone flap elevator",
            "Rongeurs (Leksell, Kerrison)",
            "Bipolar forceps",
            "Suction tips (Frazier, Adson)",
            "Retractors (Weitlaner, Gelpi)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Dural hooks and elevators",
            "Microscissors and microforceps",
            "Cranial nerve monitoring electrodes",
            "Intraoperative ultrasound probe",
            "Stereotactic navigation system"
        ]
    },
    
    "Cervical Spine Decompression and Fusion": {
        "category": "Neurosurgery",
        "specialty": "🧠 Neurosurgery",
        "instruments": [
            "Cervical retractor system",
            "High-speed drill with burrs",
            "Rongeurs (Leksell, Kerrison)",
            "Curettes (various sizes)",
            "Bone graft harvesting tools",
            "Cervical plate and screw system",
            "Cage implant system",
            "Bipolar forceps",
            "Suction tips (Frazier, Adson)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "C-arm fluoroscopy unit",
            "Nerve root retractors",
            "Interbody fusion devices"
        ]
    },
    
    "Laminectomy for Spinal Stenosis": {
        "category": "Neurosurgery",
        "specialty": "🧠 Neurosurgery",
        "instruments": [
            "Laminectomy retractor system",
            "High-speed drill with burrs",
            "Rongeurs (Leksell, Kerrison)",
            "Curettes (various sizes)",
            "Bone graft harvesting tools",
            "Bipolar forceps",
            "Suction tips (Frazier, Adson)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "C-arm fluoroscopy unit",
            "Nerve root retractors",
            "Spinal monitoring system"
        ]
    },
    
    "Aneurysm Clipping": {
        "category": "Neurosurgery",
        "specialty": "🧠 Neurosurgery",
        "instruments": [
            "Mayfield head holder and pins",
            "Craniotome with perforator and footplate",
            "Bone flap elevator",
            "Aneurysm clips and appliers",
            "Bipolar forceps",
            "Suction tips (Frazier, Adson)",
            "Retractors (Weitlaner, Gelpi)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Dural hooks and elevators",
            "Microscissors and microforceps",
            "Cranial nerve monitoring electrodes",
            "Intraoperative ultrasound probe",
            "Stereotactic navigation system"
        ]
    },
    
    "Ventriculoperitoneal (VP) Shunt Placement": {
        "category": "Neurosurgery",
        "specialty": "🧠 Neurosurgery",
        "instruments": [
            "VP shunt kit",
            "Shunt valve and tubing",
            "Burr hole instruments",
            "Bipolar forceps",
            "Suction tips (Frazier, Adson)",
            "Retractors (Weitlaner, Gelpi)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Dural hooks and elevators",
            "Microscissors and microforceps",
            "Cranial nerve monitoring electrodes",
            "Intraoperative ultrasound probe",
            "Stereotactic navigation system"
        ]
    },
    
    # ❤️ Cardiothoracic Surgery
    "Coronary Artery Bypass Grafting (CABG)": {
        "category": "Cardiothoracic",
        "specialty": "❤️ Cardiothoracic Surgery",
        "instruments": [
            "Sternal saw and retractor",
            "Internal mammary artery retractor",
            "Coronary artery stabilizer",
            "Vessel loops and bulldog clamps",
            "Coronary scissors and forceps",
            "Saphenous vein harvesting tools",
            "Aortic punch and side-biting clamp",
            "Cardioplegia delivery system",
            "Chest tube insertion kit",
            "Sternal wires and wire twisters",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Pacemaker wires",
            "Chest drainage system"
        ]
    },
    
    "Mitral or Aortic Valve Replacement": {
        "category": "Cardiothoracic",
        "specialty": "❤️ Cardiothoracic Surgery",
        "instruments": [
            "Sternal saw and retractor",
            "Valve sizers and holders",
            "Valve excision tools",
            "Annuloplasty ring system",
            "Sutures (2-0, 3-0 Prolene)",
            "Cardioplegia delivery system",
            "Aortic cross-clamp",
            "Left atrial retractor",
            "Valve testing apparatus",
            "Chest tube insertion kit",
            "Sternal wires and wire twisters",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Transesophageal echocardiography probe"
        ]
    },
    
    "Lobectomy (lung resection)": {
        "category": "Cardiothoracic",
        "specialty": "❤️ Cardiothoracic Surgery",
        "instruments": [
            "Thoracotomy instruments",
            "Lung retractors",
            "Bronchus stapler",
            "Vessel staplers",
            "Chest tube insertion kit",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0 Vicryl, PDS)",
            "Chest drainage system",
            "Lung isolation devices"
        ]
    },
    
    "Thoracotomy with Pleural Decortication": {
        "category": "Cardiothoracic",
        "specialty": "❤️ Cardiothoracic Surgery",
        "instruments": [
            "Thoracotomy instruments",
            "Pleural decortication instruments",
            "Chest tube insertion kit",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0 Vicryl, PDS)",
            "Chest drainage system",
            "Lung retractors"
        ]
    },
    
    "Video-Assisted Thoracoscopic Surgery (VATS)": {
        "category": "Cardiothoracic",
        "specialty": "❤️ Cardiothoracic Surgery",
        "instruments": [
            "Thoracoscope (0° and 30°)",
            "VATS instruments",
            "Endoscopic staplers",
            "Chest tube insertion kit",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0 Vicryl, PDS)",
            "Chest drainage system",
            "Thoracoscopic camera and light source"
        ]
    },
    
    # 🩺 General Surgery
    "Laparoscopic Cholecystectomy (gallbladder removal)": {
        "category": "General Surgery",
        "specialty": "🩺 General Surgery",
        "instruments": [
            "Laparoscope (0° and 30°)",
            "Trocars (5mm, 10mm, 12mm)",
            "Veress needle",
            "Laparoscopic grasper (Maryland, Babcock)",
            "Laparoscopic scissors",
            "Laparoscopic hook/spatula",
            "Clip applier",
            "Suction-irrigator",
            "Specimen retrieval bag",
            "Endoscopic stapler",
            "Laparoscopic camera and light source",
            "Insufflation tubing",
            "CO2 insufflator",
            "Laparoscopic liver retractor",
            "Laparoscopic cholangiogram catheter",
            "Laparoscopic cholangiogram kit"
        ]
    },
    
    "Laparoscopic Appendectomy": {
        "category": "General Surgery",
        "specialty": "🩺 General Surgery",
        "instruments": [
            "Laparoscope (0° and 30°)",
            "Trocars (5mm, 10mm, 12mm)",
            "Veress needle",
            "Laparoscopic grasper (Maryland, Babcock)",
            "Laparoscopic scissors",
            "Laparoscopic hook/spatula",
            "Clip applier",
            "Suction-irrigator",
            "Specimen retrieval bag",
            "Endoscopic stapler",
            "Laparoscopic camera and light source",
            "Insufflation tubing",
            "CO2 insufflator",
            "Laparoscopic retractor",
            "Laparoscopic irrigation system"
        ]
    },
    
    "Hernia Repair (Inguinal or Ventral)": {
        "category": "General Surgery",
        "specialty": "🩺 General Surgery",
        "instruments": [
            "Hernia mesh",
            "Mesh fixation devices",
            "Hernia retractors",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (0, 2-0, 3-0 Vicryl, PDS)",
            "Tissue forceps (Allis, Babcock)",
            "Abdominal retractor system"
        ]
    },
    
    "Colectomy (partial or total)": {
        "category": "General Surgery",
        "specialty": "🩺 General Surgery",
        "instruments": [
            "Bowel staplers",
            "Colon retractors",
            "Bowel clamps",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (0, 2-0, 3-0 Vicryl, PDS)",
            "Abdominal retractor system",
            "Specimen containers"
        ]
    },
    
    "Gastrectomy (partial or full stomach removal)": {
        "category": "General Surgery",
        "specialty": "🩺 General Surgery",
        "instruments": [
            "Bowel staplers",
            "Gastric retractors",
            "Bowel clamps",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (0, 2-0, 3-0 Vicryl, PDS)",
            "Abdominal retractor system",
            "Specimen containers"
        ]
    },
    
    # ⚕️ Gynecologic Surgery
    "Total Abdominal Hysterectomy (TAH)": {
        "category": "Gynecology",
        "specialty": "⚕️ Gynecologic Surgery",
        "instruments": [
            "Abdominal retractor system",
            "Uterine manipulator",
            "Vaginal retractors",
            "Uterine artery clamps",
            "Fallopian tube forceps",
            "Ovarian ligament clamps",
            "Vaginal cuff closure instruments",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (0, 2-0, 3-0 Vicryl, PDS)",
            "Foley catheter",
            "Abdominal packing",
            "Specimen container"
        ]
    },
    
    "Laparoscopic Oophorectomy (ovary removal)": {
        "category": "Gynecology",
        "specialty": "⚕️ Gynecologic Surgery",
        "instruments": [
            "Laparoscope (0° and 30°)",
            "Trocars (5mm, 10mm, 12mm)",
            "Veress needle",
            "Laparoscopic grasper (Maryland, Babcock)",
            "Laparoscopic scissors",
            "Laparoscopic hook/spatula",
            "Clip applier",
            "Suction-irrigator",
            "Specimen retrieval bag",
            "Endoscopic stapler",
            "Laparoscopic camera and light source",
            "Insufflation tubing",
            "CO2 insufflator",
            "Laparoscopic retractor",
            "Laparoscopic irrigation system"
        ]
    },
    
    "Myomectomy (fibroid removal)": {
        "category": "Gynecology",
        "specialty": "⚕️ Gynecologic Surgery",
        "instruments": [
            "Myoma screw",
            "Uterine manipulator",
            "Vaginal retractors",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (0, 2-0, 3-0 Vicryl, PDS)",
            "Abdominal retractor system",
            "Specimen container"
        ]
    },
    
    "Endometrial Ablation": {
        "category": "Gynecology",
        "specialty": "⚕️ Gynecologic Surgery",
        "instruments": [
            "Hysteroscope",
            "Endometrial ablation device",
            "Uterine manipulator",
            "Vaginal retractors",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0 Vicryl, PDS)",
            "Hysteroscopic camera and light source"
        ]
    },
    
    "Cesarean Section (C-Section)": {
        "category": "Gynecology",
        "specialty": "⚕️ Gynecologic Surgery",
        "instruments": [
            "Cesarean section instruments",
            "Uterine stapler",
            "Abdominal retractor system",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (0, 2-0, 3-0 Vicryl, PDS)",
            "Foley catheter",
            "Abdominal packing",
            "Neonatal resuscitation equipment"
        ]
    },
    
    # 🧔‍♂️ Urologic Surgery
    "Transurethral Resection of the Prostate (TURP)": {
        "category": "Urology",
        "specialty": "🧔‍♂️ Urologic Surgery",
        "instruments": [
            "Resectoscope with loop electrode",
            "Continuous flow irrigation system",
            "Electrosurgical unit",
            "Bladder irrigation fluid",
            "Foley catheter",
            "Urethral dilators",
            "Cystoscope",
            "Resectoscope bridge",
            "Tissue retrieval system",
            "Irrigation tubing",
            "Electrode cleaning stone",
            "Lubricating jelly",
            "Specimen container",
            "Urethral catheterization kit"
        ]
    },
    
    "Radical Prostatectomy": {
        "category": "Urology",
        "specialty": "🧔‍♂️ Urologic Surgery",
        "instruments": [
            "Prostatectomy instruments",
            "Urethral anastomosis instruments",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0 Vicryl, PDS)",
            "Abdominal retractor system",
            "Foley catheter",
            "Specimen container",
            "Nerve monitoring system"
        ]
    },
    
    "Nephrectomy (kidney removal)": {
        "category": "Urology",
        "specialty": "🧔‍♂️ Urologic Surgery",
        "instruments": [
            "Nephrectomy instruments",
            "Renal artery clamps",
            "Renal vein clamps",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0 Vicryl, PDS)",
            "Abdominal retractor system",
            "Foley catheter",
            "Specimen container"
        ]
    },
    
    "Ureteroscopy with Stone Removal": {
        "category": "Urology",
        "specialty": "🧔‍♂️ Urologic Surgery",
        "instruments": [
            "Ureteroscope",
            "Stone retrieval basket",
            "Laser lithotripsy device",
            "Ureteral access sheath",
            "Guidewire",
            "Ureteral stent",
            "Foley catheter",
            "Irrigation system",
            "Ureteroscopic camera and light source",
            "Stone analysis kit"
        ]
    },
    
    "Cystectomy (bladder removal)": {
        "category": "Urology",
        "specialty": "🧔‍♂️ Urologic Surgery",
        "instruments": [
            "Cystectomy instruments",
            "Ileal conduit instruments",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0 Vicryl, PDS)",
            "Abdominal retractor system",
            "Foley catheter",
            "Specimen container",
            "Ostomy supplies"
        ]
    },
    
    # 🧠 ENT / Otolaryngology
    "Tonsillectomy and Adenoidectomy": {
        "category": "ENT",
        "specialty": "🧠 ENT / Otolaryngology",
        "instruments": [
            "Mouth gag (Boyle-Davis)",
            "Tonsil snare",
            "Tonsil forceps",
            "Adenoid curettes",
            "Adenoid punch",
            "Suction tips (Frazier, Yankauer)",
            "Bipolar forceps",
            "Scalpel handles (#3) with blades (#12, #15)",
            "Scissors (Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0 Vicryl)",
            "Tonsil sponges",
            "Nasal packing",
            "Specimen containers"
        ]
    },
    
    "Functional Endoscopic Sinus Surgery (FESS)": {
        "category": "ENT",
        "specialty": "🧠 ENT / Otolaryngology",
        "instruments": [
            "Endoscope (0°, 30°, 45°, 70°)",
            "Sinus instruments",
            "Microdebrider",
            "Suction tips (Frazier, Yankauer)",
            "Bipolar forceps",
            "Scalpel handles (#3) with blades (#12, #15)",
            "Scissors (Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0 Vicryl)",
            "Nasal packing",
            "Endoscopic camera and light source"
        ]
    },
    
    "Mastoidectomy": {
        "category": "ENT",
        "specialty": "🧠 ENT / Otolaryngology",
        "instruments": [
            "Mastoid instruments",
            "Drill system with bits",
            "Suction tips (Frazier, Yankauer)",
            "Bipolar forceps",
            "Scalpel handles (#3) with blades (#12, #15)",
            "Scissors (Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0 Vicryl)",
            "Ear packing",
            "Facial nerve monitoring system"
        ]
    },
    
    "Laryngectomy (partial/total)": {
        "category": "ENT",
        "specialty": "🧠 ENT / Otolaryngology",
        "instruments": [
            "Laryngectomy instruments",
            "Tracheostomy kit",
            "Suction tips (Frazier, Yankauer)",
            "Bipolar forceps",
            "Scalpel handles (#3) with blades (#12, #15)",
            "Scissors (Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0 Vicryl, PDS)",
            "Tracheostomy tube",
            "Specimen container"
        ]
    },
    
    "Cochlear Implant Surgery": {
        "category": "ENT",
        "specialty": "🧠 ENT / Otolaryngology",
        "instruments": [
            "Cochlear implant kit",
            "Drill system with bits",
            "Suction tips (Frazier, Yankauer)",
            "Bipolar forceps",
            "Scalpel handles (#3) with blades (#12, #15)",
            "Scissors (Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0 Vicryl)",
            "Ear packing",
            "Facial nerve monitoring system",
            "Cochlear implant processor"
        ]
    },
    
    # 👁️ Ophthalmology
    "Cataract Extraction with IOL Implant": {
        "category": "Ophthalmology",
        "specialty": "👁️ Ophthalmology",
        "instruments": [
            "Phacoemulsification machine",
            "Phaco handpiece and tips",
            "IOL injector system",
            "Capsulorhexis forceps",
            "Lens nucleus chopper",
            "IOL dialer",
            "Viscoelastic solutions",
            "Irrigation/aspiration handpiece",
            "Keratome",
            "Speculum",
            "Microscissors",
            "Microforceps",
            "Capsule polisher",
            "IOL lens holder",
            "Intraocular pressure measurement device"
        ]
    },
    
    "Retinal Detachment Repair (Scleral Buckling or Vitrectomy)": {
        "category": "Ophthalmology",
        "specialty": "👁️ Ophthalmology",
        "instruments": [
            "Vitrectomy machine",
            "Vitrector handpiece",
            "Endoilluminator",
            "Retinal forceps",
            "Retinal scissors",
            "Scleral buckle",
            "Cryoprobe",
            "Laser photocoagulation device",
            "Speculum",
            "Microscissors",
            "Microforceps",
            "Intraocular pressure measurement device"
        ]
    },
    
    "Glaucoma Trabeculectomy": {
        "category": "Ophthalmology",
        "specialty": "👁️ Ophthalmology",
        "instruments": [
            "Trabeculectomy instruments",
            "Mitomycin C",
            "5-Fluorouracil",
            "Speculum",
            "Microscissors",
            "Microforceps",
            "Intraocular pressure measurement device",
            "Gonioscopy lens",
            "Scleral flap instruments"
        ]
    },
    
    "Enucleation (eye removal)": {
        "category": "Ophthalmology",
        "specialty": "👁️ Ophthalmology",
        "instruments": [
            "Enucleation instruments",
            "Orbital implant",
            "Speculum",
            "Microscissors",
            "Microforceps",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (4-0, 5-0 Vicryl, PDS)",
            "Eye patch",
            "Specimen container"
        ]
    },
    
    # 🦷 Oral & Maxillofacial Surgery
    "Mandibular Fracture Open Reduction and Internal Fixation (ORIF)": {
        "category": "Oral Surgery",
        "specialty": "🦷 Oral & Maxillofacial Surgery",
        "instruments": [
            "Maxillomandibular fixation (MMF) arch bars",
            "Wire twisters and cutters",
            "Bone reduction forceps",
            "Bone plates and screws",
            "Drill system with bits",
            "Bone holding forceps",
            "Rongeurs",
            "Bone files",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0 Vicryl, PDS)",
            "Dental instruments",
            "Temporomandibular joint instruments",
            "Facial nerve monitoring system"
        ]
    },
    
    "Le Fort Osteotomy": {
        "category": "Oral Surgery",
        "specialty": "🦷 Oral & Maxillofacial Surgery",
        "instruments": [
            "Osteotomy instruments",
            "Bone saw with blades",
            "Bone reduction forceps",
            "Bone plates and screws",
            "Drill system with bits",
            "Bone holding forceps",
            "Rongeurs",
            "Bone files",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0 Vicryl, PDS)",
            "Dental instruments",
            "Facial nerve monitoring system"
        ]
    },
    
    "Temporomandibular Joint (TMJ) Arthroplasty": {
        "category": "Oral Surgery",
        "specialty": "🦷 Oral & Maxillofacial Surgery",
        "instruments": [
            "TMJ instruments",
            "Joint replacement components",
            "Bone reduction forceps",
            "Bone plates and screws",
            "Drill system with bits",
            "Bone holding forceps",
            "Rongeurs",
            "Bone files",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0 Vicryl, PDS)",
            "Dental instruments",
            "Facial nerve monitoring system"
        ]
    },
    
    "Impacted Wisdom Tooth Extraction (OR-based)": {
        "category": "Oral Surgery",
        "specialty": "🦷 Oral & Maxillofacial Surgery",
        "instruments": [
            "Dental extraction instruments",
            "Bone removal instruments",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0 Vicryl, PDS)",
            "Dental instruments",
            "Specimen container"
        ]
    },
    
    "Cyst Enucleation or Jaw Tumor Removal": {
        "category": "Oral Surgery",
        "specialty": "🦷 Oral & Maxillofacial Surgery",
        "instruments": [
            "Cyst enucleation instruments",
            "Bone reduction forceps",
            "Bone plates and screws",
            "Drill system with bits",
            "Bone holding forceps",
            "Rongeurs",
            "Bone files",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0 Vicryl, PDS)",
            "Dental instruments",
            "Facial nerve monitoring system",
            "Specimen container"
        ]
    },
    
    # 🧴 Plastic & Reconstructive Surgery
    "Abdominoplasty (Tummy Tuck)": {
        "category": "Plastic Surgery",
        "specialty": "🧴 Plastic & Reconstructive Surgery",
        "instruments": [
            "Abdominal retractor system",
            "Liposuction cannulas",
            "Tissue forceps (Allis, Babcock)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0, 4-0 Vicryl, PDS)",
            "Drains (Jackson-Pratt)",
            "Compression garment",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Tissue markers",
            "Measuring devices",
            "Skin hooks",
            "Tissue expanders"
        ]
    },
    
    "Breast Augmentation or Reconstruction (with flaps or implants)": {
        "category": "Plastic Surgery",
        "specialty": "🧴 Plastic & Reconstructive Surgery",
        "instruments": [
            "Breast retractor system",
            "Breast implants",
            "Tissue forceps (Allis, Babcock)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0, 4-0 Vicryl, PDS)",
            "Drains (Jackson-Pratt)",
            "Compression garment",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Tissue markers",
            "Measuring devices",
            "Skin hooks",
            "Tissue expanders"
        ]
    },
    
    "Rhinoplasty (nasal reconstruction)": {
        "category": "Plastic Surgery",
        "specialty": "🧴 Plastic & Reconstructive Surgery",
        "instruments": [
            "Rhinoplasty instruments",
            "Nasal retractors",
            "Tissue forceps (Allis, Babcock)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0, 5-0 Vicryl, PDS)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Tissue markers",
            "Measuring devices",
            "Skin hooks",
            "Nasal packing"
        ]
    },
    
    "Skin Graft Harvesting and Placement": {
        "category": "Plastic Surgery",
        "specialty": "🧴 Plastic & Reconstructive Surgery",
        "instruments": [
            "Dermatome",
            "Skin graft mesher",
            "Tissue forceps (Allis, Babcock)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0, 5-0 Vicryl, PDS)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Tissue markers",
            "Measuring devices",
            "Skin hooks",
            "Graft dressing materials"
        ]
    },
    
    "Cleft Lip/Palate Repair": {
        "category": "Plastic Surgery",
        "specialty": "🧴 Plastic & Reconstructive Surgery",
        "instruments": [
            "Cleft repair instruments",
            "Oral retractors",
            "Tissue forceps (Allis, Babcock)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0, 5-0 Vicryl, PDS)",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Bipolar forceps",
            "Suction tips (Yankauer, Poole)",
            "Tissue markers",
            "Measuring devices",
            "Skin hooks",
            "Dental instruments"
        ]
    },
    
    # 🦴 Orthopedic Surgery
    "Total Knee Arthroplasty (TKA)": {
        "category": "Orthopedics",
        "specialty": "🦴 Orthopedic Surgery",
        "instruments": [
            "Knee retractor system",
            "Bone cutting jigs",
            "Osteotomes",
            "Bone saw with blades",
            "Trial components",
            "Cement mixing system",
            "Pulse lavage system",
            "Tourniquet system",
            "Bone cement",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (0, 2-0, 3-0 Vicryl, PDS)",
            "Drains (Hemovac)",
            "Compression bandage",
            "C-arm fluoroscopy unit"
        ]
    },
    
    "Total Hip Arthroplasty (THA)": {
        "category": "Orthopedics",
        "specialty": "🦴 Orthopedic Surgery",
        "instruments": [
            "Hip retractor system",
            "Bone cutting jigs",
            "Osteotomes",
            "Bone saw with blades",
            "Trial components",
            "Cement mixing system",
            "Pulse lavage system",
            "Bone cement",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (0, 2-0, 3-0 Vicryl, PDS)",
            "Drains (Hemovac)",
            "Compression bandage",
            "C-arm fluoroscopy unit",
            "Hip dislocation instruments"
        ]
    },
    
    "Anterior Cruciate Ligament (ACL) Reconstruction": {
        "category": "Orthopedics",
        "specialty": "🦴 Orthopedic Surgery",
        "instruments": [
            "Arthroscope (0° and 30°)",
            "Arthroscopic shaver",
            "ACL reconstruction instruments",
            "Graft harvesting tools",
            "Tibial and femoral tunnel guides",
            "Interference screws",
            "Endobutton",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0 Vicryl, PDS)",
            "Arthroscopic camera and light source",
            "Tourniquet system",
            "Compression bandage"
        ]
    },
    
    "Open Reduction Internal Fixation (ORIF) of Tibia/Femur": {
        "category": "Orthopedics",
        "specialty": "🦴 Orthopedic Surgery",
        "instruments": [
            "Bone reduction forceps",
            "Bone plates and screws",
            "Drill system with bits",
            "Bone holding forceps",
            "Rongeurs",
            "Bone files",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0 Vicryl, PDS)",
            "C-arm fluoroscopy unit",
            "Tourniquet system",
            "Compression bandage",
            "Bone graft materials"
        ]
    },
    
    "Shoulder Arthroscopy with Rotator Cuff Repair": {
        "category": "Orthopedics",
        "specialty": "🦴 Orthopedic Surgery",
        "instruments": [
            "Arthroscope (0° and 30°)",
            "Arthroscopic shaver",
            "Rotator cuff repair instruments",
            "Suture anchors",
            "Arthroscopic suturing devices",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (2-0, 3-0 Vicryl, PDS)",
            "Arthroscopic camera and light source",
            "Tourniquet system",
            "Compression bandage",
            "Shoulder positioning device"
        ]
    },
    
    "Carpal Tunnel Release (open or endoscopic)": {
        "category": "Orthopedics",
        "specialty": "🦴 Orthopedic Surgery",
        "instruments": [
            "Carpal tunnel release instruments",
            "Endoscopic carpal tunnel release kit",
            "Nerve decompression instruments",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0 Vicryl, PDS)",
            "Tourniquet system",
            "Compression bandage",
            "Nerve monitoring system"
        ]
    },
    
    # 🩹 Dermatologic Surgery
    "Wide Local Excision of Skin Cancer (e.g., melanoma)": {
        "category": "Dermatology",
        "specialty": "🩹 Dermatologic Surgery",
        "instruments": [
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Skin hooks",
            "Tissue forceps (Adson, DeBakey)",
            "Scissors (Mayo, Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0, 5-0 Vicryl, PDS, Prolene)",
            "Skin stapler",
            "Tissue markers",
            "Measuring devices",
            "Specimen containers",
            "Mohs micrographic surgery equipment",
            "Frozen section equipment",
            "Dermatoscope",
            "Local anesthesia kit",
            "Electrosurgical unit"
        ]
    },
    
    "Mohs Micrographic Surgery (advanced cases)": {
        "category": "Dermatology",
        "specialty": "🩹 Dermatologic Surgery",
        "instruments": [
            "Mohs surgery instruments",
            "Frozen section equipment",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Skin hooks",
            "Tissue forceps (Adson, DeBakey)",
            "Scissors (Mayo, Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0, 5-0 Vicryl, PDS, Prolene)",
            "Skin stapler",
            "Tissue markers",
            "Measuring devices",
            "Specimen containers",
            "Dermatoscope",
            "Local anesthesia kit",
            "Electrosurgical unit"
        ]
    },
    
    "Skin Flap Reconstruction for Large Defects": {
        "category": "Dermatology",
        "specialty": "🩹 Dermatologic Surgery",
        "instruments": [
            "Skin flap instruments",
            "Dermatome",
            "Skin graft mesher",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Skin hooks",
            "Tissue forceps (Adson, DeBakey)",
            "Scissors (Mayo, Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0, 5-0 Vicryl, PDS, Prolene)",
            "Skin stapler",
            "Tissue markers",
            "Measuring devices",
            "Specimen containers",
            "Local anesthesia kit",
            "Electrosurgical unit"
        ]
    },
    
    "Full-thickness Skin Biopsy in OR (immunosuppressed patients)": {
        "category": "Dermatology",
        "specialty": "🩹 Dermatologic Surgery",
        "instruments": [
            "Skin biopsy instruments",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Skin hooks",
            "Tissue forceps (Adson, DeBakey)",
            "Scissors (Mayo, Metzenbaum, Iris)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Sutures (3-0, 4-0, 5-0 Vicryl, PDS, Prolene)",
            "Skin stapler",
            "Tissue markers",
            "Measuring devices",
            "Specimen containers",
            "Local anesthesia kit",
            "Electrosurgical unit"
        ]
    },
    
    # 🔬 Vascular Surgery
    "Carotid Endarterectomy": {
        "category": "Vascular",
        "specialty": "🔬 Vascular Surgery",
        "instruments": [
            "Vascular clamps (Fogarty, Satinsky)",
            "Vascular forceps (DeBakey, Gerald)",
            "Vascular scissors",
            "Vascular sutures (5-0, 6-0, 7-0 Prolene)",
            "Patch material",
            "Vascular shunts",
            "Doppler ultrasound probe",
            "Intraoperative angiography equipment",
            "Heparin solution",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Vascular loops",
            "Vessel dilators",
            "Vascular graft material"
        ]
    },
    
    "Femoral-Popliteal Bypass": {
        "category": "Vascular",
        "specialty": "🔬 Vascular Surgery",
        "instruments": [
            "Vascular clamps (Fogarty, Satinsky)",
            "Vascular forceps (DeBakey, Gerald)",
            "Vascular scissors",
            "Vascular sutures (5-0, 6-0, 7-0 Prolene)",
            "Vascular graft material",
            "Doppler ultrasound probe",
            "Intraoperative angiography equipment",
            "Heparin solution",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Vascular loops",
            "Vessel dilators"
        ]
    },
    
    "Endovascular Aneurysm Repair (EVAR)": {
        "category": "Vascular",
        "specialty": "🔬 Vascular Surgery",
        "instruments": [
            "Endovascular stent graft",
            "Guidewire",
            "Catheters",
            "Angioplasty balloons",
            "Intraoperative angiography equipment",
            "Heparin solution",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Vascular loops",
            "Vessel dilators",
            "Doppler ultrasound probe"
        ]
    },
    
    "Arteriovenous (AV) Fistula Creation for Dialysis": {
        "category": "Vascular",
        "specialty": "🔬 Vascular Surgery",
        "instruments": [
            "Vascular clamps (Fogarty, Satinsky)",
            "Vascular forceps (DeBakey, Gerald)",
            "Vascular scissors",
            "Vascular sutures (5-0, 6-0, 7-0 Prolene)",
            "Doppler ultrasound probe",
            "Heparin solution",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Vascular loops",
            "Vessel dilators"
        ]
    },
    
    "Embolectomy / Thrombectomy": {
        "category": "Vascular",
        "specialty": "🔬 Vascular Surgery",
        "instruments": [
            "Fogarty balloon catheter",
            "Vascular clamps (Fogarty, Satinsky)",
            "Vascular forceps (DeBakey, Gerald)",
            "Vascular scissors",
            "Vascular sutures (5-0, 6-0, 7-0 Prolene)",
            "Doppler ultrasound probe",
            "Intraoperative angiography equipment",
            "Heparin solution",
            "Scalpel handles (#3, #7) with blades (#10, #11, #15)",
            "Scissors (Mayo, Metzenbaum)",
            "Hemostatic agents (Surgicel, Gelfoam)",
            "Vascular loops",
            "Vessel dilators"
        ]
    },
    
    # 🧒 Pediatric Surgery
    "Pyloromyotomy for Pyloric Stenosis": {
        "category": "Pediatric",
        "specialty": "🧒 Pediatric Surgery",
        "instruments": [
            "Pediatric retractor system",
            "Pediatric forceps (DeBakey, Gerald)",
            "Pediatric scissors (Mayo, Metzenbaum)",
            "Pediatric scalpel handles (#3) with blades (#10, #11, #15)",
            "Pediatric sutures (4-0, 5-0 Vicryl, PDS)",
            "Pediatric hemostatic agents (Surgicel, Gelfoam)",
            "Pediatric suction tips",
            "Pediatric bipolar forceps",
            "Pediatric abdominal instruments",
            "Pediatric measuring devices",
            "Pediatric specimen containers",
            "Pediatric anesthesia equipment",
            "Pediatric monitoring equipment",
            "Pediatric warming devices",
            "Pediatric positioning equipment"
        ]
    },
    
    "Congenital Diaphragmatic Hernia Repair": {
        "category": "Pediatric",
        "specialty": "🧒 Pediatric Surgery",
        "instruments": [
            "Pediatric retractor system",
            "Pediatric forceps (DeBakey, Gerald)",
            "Pediatric scissors (Mayo, Metzenbaum)",
            "Pediatric scalpel handles (#3) with blades (#10, #11, #15)",
            "Pediatric sutures (4-0, 5-0 Vicryl, PDS)",
            "Pediatric hemostatic agents (Surgicel, Gelfoam)",
            "Pediatric suction tips",
            "Pediatric bipolar forceps",
            "Pediatric abdominal instruments",
            "Pediatric measuring devices",
            "Pediatric specimen containers",
            "Pediatric anesthesia equipment",
            "Pediatric monitoring equipment",
            "Pediatric warming devices",
            "Pediatric positioning equipment"
        ]
    },
    
    "Imperforate Anus Correction": {
        "category": "Pediatric",
        "specialty": "🧒 Pediatric Surgery",
        "instruments": [
            "Pediatric retractor system",
            "Pediatric forceps (DeBakey, Gerald)",
            "Pediatric scissors (Mayo, Metzenbaum)",
            "Pediatric scalpel handles (#3) with blades (#10, #11, #15)",
            "Pediatric sutures (4-0, 5-0 Vicryl, PDS)",
            "Pediatric hemostatic agents (Surgicel, Gelfoam)",
            "Pediatric suction tips",
            "Pediatric bipolar forceps",
            "Pediatric abdominal instruments",
            "Pediatric measuring devices",
            "Pediatric specimen containers",
            "Pediatric anesthesia equipment",
            "Pediatric monitoring equipment",
            "Pediatric warming devices",
            "Pediatric positioning equipment"
        ]
    },
    
    "Omphalocele or Gastroschisis Repair": {
        "category": "Pediatric",
        "specialty": "🧒 Pediatric Surgery",
        "instruments": [
            "Pediatric retractor system",
            "Pediatric forceps (DeBakey, Gerald)",
            "Pediatric scissors (Mayo, Metzenbaum)",
            "Pediatric scalpel handles (#3) with blades (#10, #11, #15)",
            "Pediatric sutures (4-0, 5-0 Vicryl, PDS)",
            "Pediatric hemostatic agents (Surgicel, Gelfoam)",
            "Pediatric suction tips",
            "Pediatric bipolar forceps",
            "Pediatric abdominal instruments",
            "Pediatric measuring devices",
            "Pediatric specimen containers",
            "Pediatric anesthesia equipment",
            "Pediatric monitoring equipment",
            "Pediatric warming devices",
            "Pediatric positioning equipment"
        ]
    },
    
    "Pediatric Appendectomy": {
        "category": "Pediatric",
        "specialty": "🧒 Pediatric Surgery",
        "instruments": [
            "Pediatric retractor system",
            "Pediatric forceps (DeBakey, Gerald)",
            "Pediatric scissors (Mayo, Metzenbaum)",
            "Pediatric scalpel handles (#3) with blades (#10, #11, #15)",
            "Pediatric sutures (4-0, 5-0 Vicryl, PDS)",
            "Pediatric hemostatic agents (Surgicel, Gelfoam)",
            "Pediatric suction tips",
            "Pediatric bipolar forceps",
            "Pediatric abdominal instruments",
            "Pediatric measuring devices",
            "Pediatric specimen containers",
            "Pediatric anesthesia equipment",
            "Pediatric monitoring equipment",
            "Pediatric warming devices",
            "Pediatric positioning equipment"
        ]
    }
}

# Common surgical instruments that appear across multiple procedures
COMMON_SURGICAL_INSTRUMENTS = {
    "cutting_instruments": [
        "Scalpel handles (#3, #7) with blades (#10, #11, #12, #15)",
        "Scissors: Mayo scissors (straight, curved)",
        "Scissors: Metzenbaum scissors (fine, curved/straight)",
        "Scissors: Iris scissors",
        "Osteotomes, rongeurs, Gigli saws (orthopedics)"
    ],
    
    "forceps_grasping": [
        "Tissue forceps: Allis, Babcock, Debakey, Adson (various sizes)",
        "Mosquito forceps, Kelly, Crile, Rochester–Pean hemostats",
        "Russian forceps, toothed and non-toothed variants"
    ],
    
    "needle_holders_suturing": [
        "Mayo–Hegar needle holders, Webster needle holders, Castroviejo",
        "Suture sets: Absorbable: Vicryl, PDS, Monocryl, Chromic gut",
        "Suture sets: Non‑absorbable: Silk, Nylon, Prolene"
    ],
    
    "clamps_tissue_manipulators": [
        "Towel clamps (Backhaus, Lorna), Kelly clamps",
        "Refined surgical hooks (Richardson, Deaver, Weitlaner self-retaining retractors)",
        "Army‑Navy, Ribbon, Langenbeck, Richardson‑Eastman retractors"
    ],
    
    "electrosurgical_energy_devices": [
        "Bovie (monopolar pencil, hook, spatula)",
        "Bipolar forceps, LigaSure, ultrasonic Harmonic scalpel (ultrasonic cutting/sealing)"
    ],
    
    "laparoscopic_instruments": [
        "Trocars (5 mm, 10–11 mm), Veress needle, Hasson trocar",
        "Laparoscope (0°/30°), insufflation tubing, light source and camera",
        "Atraumatic graspers, Maryland dissector, laparoscopic scissors, hook/spatula, clip applier, suction-irrigator, retrieval pouch",
        "Morcellator (for urologic or gynecologic laparoscopic resection)"
    ],
    
    "suction_irrigation": [
        "Yankauer suction, Poole suction, Frazier tip, suction-irrigator sets"
    ],
    
    "ancillary_supplies_consumables": [
        "Gallipot cups, kidney trays (for fluids, specimens)",
        "Sterile drapes, sponge holding forceps, surgical sponges/swabs, sharps container",
        "Tip protectors and stringers",
        "Sterile gloves, towel clips, labels, suture packets, sharps count documentation"
    ],
    
    "staplers_clips_hemostatic": [
        "Linear GIA staplers",
        "Surgical clips and appliers (for vessels/ducts)",
        "Sponge holders, specimen retrieval pouches"
    ]
}

def get_all_surgical_procedures():
    """Get all available surgical procedures"""
    return list(SURGICAL_PROCEDURES.keys())

def get_procedures_by_specialty():
    """Get procedures organized by surgical specialty"""
    specialty_procedures = {}
    for procedure, data in SURGICAL_PROCEDURES.items():
        specialty = data['specialty']
        if specialty not in specialty_procedures:
            specialty_procedures[specialty] = []
        specialty_procedures[specialty].append(procedure)
    return specialty_procedures

def get_procedure_instruments(procedure_name):
    """Get instruments required for a specific procedure"""
    return SURGICAL_PROCEDURES.get(procedure_name, {}).get('instruments', [])

def get_procedure_category(procedure_name):
    """Get the category of a specific procedure"""
    return SURGICAL_PROCEDURES.get(procedure_name, {}).get('category', '')

def get_procedure_specialty(procedure_name):
    """Get the specialty of a specific procedure"""
    return SURGICAL_PROCEDURES.get(procedure_name, {}).get('specialty', '')

def get_common_instruments():
    """Get common surgical instruments"""
    return COMMON_SURGICAL_INSTRUMENTS

def match_surgical_instrument(input_instrument):
    """Match input instrument against surgical instruments database"""
    input_lower = input_instrument.lower()
    
    # Check in procedure-specific instruments
    for procedure, data in SURGICAL_PROCEDURES.items():
        for instrument in data['instruments']:
            if input_lower in instrument.lower() or instrument.lower() in input_lower:
                return instrument
    
    # Check in common instruments
    for category, instruments in COMMON_SURGICAL_INSTRUMENTS.items():
        for instrument in instruments:
            if input_lower in instrument.lower() or instrument.lower() in input_lower:
                return instrument
    
    return None

def get_instruments_by_category():
    """Get instruments organized by category"""
    return COMMON_SURGICAL_INSTRUMENTS 
