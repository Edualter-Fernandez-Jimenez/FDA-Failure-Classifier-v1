-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-02-2026 a las 02:08:53
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `fda_code_classifier`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `event_ticket_response`
--

CREATE TABLE `event_ticket_response` (
  `response_cd` int(11) NOT NULL,
  `case_cd` varchar(20) NOT NULL,
  `event_summary_desc` text DEFAULT NULL,
  `investigation_desc` text DEFAULT NULL,
  `ia_fda_cd` varchar(10) DEFAULT NULL,
  `ia_fda_term_desc` varchar(255) DEFAULT NULL,
  `ia_fda_deff_desc` text DEFAULT NULL,
  `ia_problem_explanation_desc` text DEFAULT NULL,
  `ia_code_explanation_desc` text DEFAULT NULL,
  `create_dt` date DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `event_ticket_response` AUTO_INCREMENT = 1;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fda_annex_c`
--

CREATE TABLE `fda_annex_c` (
  `fda_cd` int(11) NOT NULL,
  `lvl_1_term` varchar(255) DEFAULT NULL,
  `lvl_2_term` varchar(255) DEFAULT NULL,
  `lvl_3_term` varchar(255) DEFAULT NULL,
  `definition_desc` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `fda_annex_c`
--

INSERT INTO `fda_annex_c` (`fda_cd`, `lvl_1_term`, `lvl_2_term`, `lvl_3_term`, `definition_desc`) VALUES
(13, NULL, 'Device Difficult to Operate', NULL, 'Problems including set-up, operation, and disassembly of equipment. Not including reprocessing.'),
(102, NULL, 'Incompatible Component/ Accessory', NULL, 'A device that malfunctions due to a component(s)/accessory that does not operate correctly and according to the device\'s specifications.'),
(104, 'Software Problem Identified', NULL, NULL, 'Problems related to the device software.'),
(110, NULL, 'Design Error', NULL, 'The device had faulty (incomplete or incorrect) software design.'),
(111, NULL, 'Packaging Problem Identified', NULL, 'Problems that occurred because of the device packaging.'),
(113, NULL, NULL, 'Interface Design Error', 'The device software was found to contain errors in the user interface (including usability problems) or the interfaces with other systems.'),
(114, 'Operational Problem Identified', NULL, NULL, 'Problems that occur during the performance, use, or functioning of the device.'),
(115, 'Maintenance Problem Identified', NULL, NULL, 'A device malfunction or problem that occurs after production because the device was not properly maintained according to the instructions (e.g. maintenance may be performed by user facility, distributor, or service provider).'),
(120, 'Electrical Problem Identified', NULL, NULL, 'Events associated with an electrically powered device where an electrical malfunction results in a device problem (e.g. electrical circuitry, contact or component failed) even if the problem is intermittent.'),
(121, NULL, 'Short Circuit', NULL, 'Problems due to an unintentionally low-resistance connection between two points in an electric circuit, resulting in either excessive current flow that often causes damage or in a new shorter circuit that draws current away from the original pathways and components.'),
(122, NULL, 'Open Circuit', NULL, 'Problem due to an electrical circuit that does not conduct current because a switch is open, a wire is broken, etc.'),
(131, NULL, NULL, 'Energy Storage System Problem', 'Problems related to the energy storage system (e.g. the rechargeable battery, charging system, or capacitor) and includes problems such as premature power source depletion and battery explosions.'),
(135, NULL, 'Degradation Problem Identified', NULL, 'Problems that occur when the device becomes worn, weakened, corroded, or broken down due to processes such as aging, permeation, and corrosion.'),
(140, NULL, NULL, 'Wear Problem', 'Problems due to the premature or expected erosion of its material by use, deterioration, or change.'),
(142, NULL, 'Biological Contamination', NULL, 'The undesirable presence of living organisms such as bacteria, fungi, or viruses or their products (enzymes or toxins).'),
(144, NULL, 'Insulation Problem Identified', NULL, 'Problems due to inadequate or incorrect electrical insulation material.'),
(145, NULL, 'Lubrication Problem Identified', NULL, 'Problems that occurred because of the presence of either too much or too little lubricant where required (e.g. connectors, leading to failure mechanisms such as corrosion).'),
(150, 'Labeling and Instructions for Use/Maintenance', NULL, NULL, 'Insufficient, inadequate, or incorrect information provided on a device\'s label or documentation regarding e.g. its intended use, directions for use, and characteristics of the device, including its maintenance.'),
(154, NULL, 'Inadequate Labelling and/or Instructions for Use', NULL, 'Inadequate information on the labels or in the instructions for use e.g. steps that are difficult to follow or that are missing.'),
(156, NULL, 'Incorrect Labeling and/or Instructions for Use', NULL, 'Missing, incorrect, or inappropriate information on the labels e.g. mislabeled contents or device labeling characteristics or package contents.'),
(170, 'Manufacturing Process Problem Identified', NULL, NULL, 'Problems with a device that can be traced to a problem in the manufacturing and/or production process.'),
(171, NULL, NULL, 'Packaging Compromised', 'Problems that occurred because of a compromised packaging of the device (e.g. broken or incomplete seal).'),
(174, 'Material and/or Chemical Problem Identified', NULL, NULL, 'Problems with the device materials or how its materials react to other elements either within the device or within the environment.'),
(176, NULL, 'Tolerance Stack-Up', NULL, 'Problems that result from a combination of specification variances of the components.'),
(180, 'Mechanical Problem Identified', NULL, NULL, 'Problems that result from internal or external forces including fluids, other objects, or environmental or physiologic influences.'),
(193, NULL, 'Storage Problem Identified', NULL, 'Problems that result from storing the device in an uncontrolled or improper environment (e.g. moisture sensitive devices stored in a humid environment).'),
(196, NULL, 'Optical Transmission Problem Identified', NULL, 'Problems with the device\'s ability to pass light energy.'),
(197, 'Electromagnetic Compatibility Problem Identified', NULL, NULL, 'Device-to-device or device-environment problem resulting from electromagnetic disturbances.'),
(202, NULL, 'Inappropriate Material', NULL, 'Problems that occur due to the presence of a material that should not be present or part of the device.'),
(203, NULL, 'Incompatible Material', NULL, 'Problems that occur due to the incompatibility of materials that co-exist simultaneously as part of the device.'),
(211, NULL, 'Hardware Timing Problem Identified', NULL, 'Problems that results from improper sequential activation of components.'),
(213, 'No Device Problem Found', NULL, NULL, 'Reported problem cannot be reproduced during investigation.'),
(323, NULL, 'Gradient Induced Field Problem', NULL, 'Problems that result from the gradient-induced fields generated during radiologic procedures e.g. magnetic resonance imaging.'),
(331, 'Environment Problem Identified', NULL, NULL, 'Problems that occurred due to factors within the environment e.g. dust, dirt, humidity, temperature.'),
(332, NULL, 'Environmental Humidity Problem Identified', NULL, 'Device performance was affected by the humidity, or changes in humidity, of the environment in which it was used.'),
(608, NULL, NULL, 'Wired Communication Problem', 'Communications problems between devices within a wired system.'),
(610, NULL, NULL, 'Loss of Power', 'A device that experienced problems due to a loss in the power supply.'),
(611, NULL, 'Radiofrequency Interference (RFI)', NULL, 'Problems due to radiofrequency interference. RFI is a disturbance that affects an electrical circuit due to either electromagnetic conduction or electromagnetic radiation emitted from an external source.'),
(618, NULL, NULL, 'Incorrect Algorithm', 'The device software was found to implement an incorrect sequence of steps for a specific computation.'),
(628, NULL, 'Communications Problem Identified', NULL, 'Devices that do not send or receive adequate signals (this speaks to the interoperability between devices).'),
(634, NULL, NULL, 'Software Timing Problem', 'Problems that results from the incorrect sequencing or activation of software modules.'),
(642, 'Thermal Problem', NULL, NULL, 'Problems related to the temperature of the device. Note: For problems related to environmental temperature use \'\'Environment Problem Identified\'\'.'),
(646, NULL, 'Dust or Dirt Problem Identified', NULL, 'A device that experienced problems due to ingress, or coating, of dust or dirt.'),
(648, NULL, 'Electrostatic Discharge', NULL, 'Problems due to sudden and momentary bursts of electrical current flowing between two objects at different electrical potentials.'),
(649, NULL, NULL, 'Vibration Problem', 'Problems caused by the constant rhythmic motion of the device, or something in the environment to which the device is exposed.'),
(650, NULL, 'Current Leakage Problem', NULL, 'Problems related to leakage currents which may cause electric shock. These currents usually flow through the protective ground conductor. In its absence, these currents could flow from the device to the ground via the human body.'),
(651, NULL, 'Environmental Temperature Problem Identified', NULL, 'Device performance was affected by the temperature, or changes in temperature, of the environment in which it was used.'),
(658, NULL, 'Conducted Interference', NULL, 'Problems related to electromagnetic interference (EMI) by physical contact with conductors (e.g. wires, resistors, terminals) as opposed to radiated EMI which is caused by induction (without physical contact of the conductors).'),
(659, NULL, NULL, 'Power Fluctuation', 'The device failed due to fluctuations within the power supply (e.g. transient power, power spike, power dip, or power sequencing).'),
(663, NULL, NULL, 'Data Compression Error', 'Data was lost or corrupted during the operation of reducing storage space or communication bandwidth.'),
(706, NULL, 'Assembly Problem Identified', NULL, 'Problems that occurred because the device was assembled incorrectly.'),
(3200, NULL, NULL, 'Incorrect Data Definition', 'The device software was found to contain errors in specifying or manipulating data items.'),
(3201, NULL, 'Installation Problem Identified', NULL, 'A device that malfunctions because it was incorrectly installed, set-up, or configured (e.g. misconfiguration of an \"automatic\" defibrillator to \"semi-automatic\", thereby leading to failure).'),
(3202, NULL, NULL, 'Agglutination Problem', 'The device affects the ability of the blood to clot which may be induced by chemical, mechanical, or thermal properties of the device.'),
(3203, NULL, 'Biocompatibility Problem Identified', NULL, 'The device causes cellular or tissue responses that elicit an undesirable local or systemic effect in the recipient or beneficiary of that therapy. (See ISO 10993)'),
(3204, 'Biological Problem Identified', NULL, NULL, 'Problems relating to, caused by or affecting biological processes or living organisms.'),
(3205, NULL, NULL, 'Carcinogenic Problem', 'The device\'s ability to trigger development of cancer.'),
(3206, NULL, NULL, 'Complement Activation Problem', 'The device affects the body\'s ability to activate the complement system of the immune system, thereby interfering with the ability to clear pathogens. This may be caused by an interaction of the device with chemicals or materials.'),
(3207, NULL, 'Device Migration', NULL, 'A device that has moved from its original location due to external forces (e.g. stent or lead movement).'),
(3208, NULL, 'Configuration Issue', NULL, 'Problems due to change control or incorrect version, including regional requirements.'),
(3211, NULL, NULL, 'Deformation Problem', 'Problems caused by changes in the shape or size of the device due to an applied force. This can be a result of tensile forces, compressive forces, shear, bending, tensile (pulling), or torsion.'),
(3212, NULL, NULL, 'Endotoxin Contamination', 'The undesirable presence of toxins associated with certain bacteria (e.g. gram negative bacteria).'),
(3213, 'Interoperability Problem Identified', NULL, NULL, 'Problems with the mechanical, electrical, or communication interface between two or more separate devices.'),
(3215, NULL, 'Magnetically-Induced Movement', NULL, 'Problems due to unintended or excessive movement created by the application of magnetic fields.'),
(3216, NULL, 'Material or Material Leachate Pyrogenic Problem', NULL, 'The undesirable presence of pyrogens or fever-producing organisms caused by materials that permeate through the device.'),
(3217, NULL, NULL, 'Mechanical Shock Problem', 'Problems caused by the sudden violent blow or collision to the whole device (e.g. by dropping).'),
(3218, NULL, NULL, 'Microbial Contamination', 'The undesirable presence of microorganisms or microbes such as bacteria and fungi (yeasts and molds).'),
(3219, NULL, NULL, 'Molecular Structure Problem', 'Problems related to the presence of an inappropriate molecular geometry somewhere in the device (i.e. the spatial arrangement of atoms in a molecule and the chemical bonds that hold the atoms together).'),
(3220, NULL, NULL, 'Mutagenic Problem', 'The device\'s ability to change genetic information (usually DNA) of an organism and thus increasing the frequency of mutations.'),
(3221, 'No Findings Available', NULL, NULL, 'Use when no investigation can be performed and therefore no results will be obtained.'),
(3222, NULL, NULL, 'Non-Functional Defect', 'The device software contained software errors that did not impact its operation.'),
(3224, 'Optical Problem Identified', NULL, NULL, 'Problems related to the optical properties of a device.'),
(3226, NULL, NULL, 'Platelet Activation Problem', 'The device affects the body\'s ability to activate platelet formation.'),
(3227, NULL, 'Power Source Problem Identified', NULL, 'Problems related to the source that provides electrical power to the device.'),
(3228, 'Protective System Problem Identified', NULL, NULL, 'Problems related to the system(s) designed to prevent or warn about unsafe operation of the device.'),
(3229, NULL, 'Radiofrequency Induced Overheating', NULL, 'Problems due to unintended radiofrequency-induced temperature increase that can occur in the vicinity of the device.'),
(3230, 'Clinical Imaging Problem Identified', NULL, NULL, 'Problems that occur with devices used for radiographic or imaging procedures e.g. CT scanners, magnetic resonance imaging.'),
(3231, NULL, 'Reactivity Problem Identified', NULL, 'Problems that occur due to the reactivity of materials (e.g. over-react or under-react).'),
(3232, NULL, 'Reproductive Toxicity Problem Identified', NULL, 'The device affects reproductive function, embryo development (teratogenicity), and prenatal and early postnatal development. (ISO 10993 part 3)'),
(3233, 'Results Pending Completion of Investigation', NULL, NULL, 'Investigation is ongoing and results are not yet available. Do not use this code if the investigation is complete.'),
(3236, NULL, 'Transport Problem Identified', NULL, 'Problems traced to how the device was transported e.g. temperature of shipping compartment or method of transportation.'),
(3237, NULL, 'Signal Loss', NULL, 'Problems due to the loss or weakening of an electrical signal or signals.'),
(3238, NULL, 'Software Installation Problem Identified', NULL, 'The device software was not installed as per the specifications or failed to properly install.'),
(3239, NULL, 'Software Requirement Error', NULL, 'The software requirements for the device are either incomplete, inadequate, or in conflict.'),
(3240, NULL, 'Software Runtime Error', NULL, 'The device software failed during operation as a result of a coding error.'),
(3241, NULL, 'Software Security Vulnerability', NULL, 'The device software failed to provide adequate authorization, access control, protection and accountability features.'),
(3242, NULL, 'Stiffness Problem Identified', NULL, 'Problems that occurred when its material is either too flexible/pliable or inflexible/rigid when in contact by an applied force.'),
(3243, NULL, 'Stress Problem Identified', NULL, 'Problems caused by either excessive or inadequate physical force exerted on it by another object resulting in problems e.g. wear, bending, deformation, fracture, fatigue.'),
(3244, NULL, NULL, 'Problem due to Thrombosis Activation', 'The device causes the formation of blood clots in or along blood vessels resulting in disturbed or disrupted blood flow.'),
(3248, NULL, NULL, 'Wireless Communication Problem', 'Communications problems between devices within a wireless system.'),
(3250, NULL, 'Failure to Calibrate or Used Out of Calibration', NULL, 'A device that cannot calibrate (establish the relationship between a measuring device and the units of measure) or is used out of calibration to ensure accurate readings.'),
(3251, NULL, NULL, 'Fatigue Problem', 'Problems due to the weakening or breakdown of its material when subjected to stress or a series of repeated stresses.'),
(3252, NULL, NULL, 'Fracture Problem', 'Problems caused by the separation of a component, object, or material into two or more pieces including shear.'),
(3253, NULL, 'Friction Problem Identified', NULL, 'Problems caused by its surface coming in contact with another surface or fluid.'),
(3254, NULL, 'Genotoxicity Problem Identified', NULL, 'The device\'s ability to cause damage to genetic material (e.g. leading to malignant tumors). (See ISO 10993)'),
(3255, NULL, 'Hematological Problem Identified', NULL, 'The device affects or impacts the blood or its components. (See ISO 10993 all parts)'),
(3256, NULL, 'Image Artifact', NULL, 'The unacceptable distortion of an image due to signal loss that may occur during a radiologic procedure such as magnetic resonance imaging.'),
(3257, NULL, 'Impedance Problem Identified', NULL, 'Problems due to insufficient or excessive resistance to current flow either by the device or circuit.'),
(3258, NULL, NULL, 'Improper Composition/ Concentration', 'Problems associated with the improper combination of materials or elements present in the device (e.g. improper composition of the materials of a capacitor).'),
(3259, NULL, NULL, 'Improper Physical Structure', 'Problems related to the incorrect or inadequate arrangement of the parts, components, elements, or materials.'),
(3260, NULL, 'Inadequate Immunity', NULL, 'Problems related to immunity or capabilities to resist electromagnetic interference (EMI).'),
(4201, NULL, 'Cytotoxicity Problem Identified', NULL, 'The device was found to have an undesirable level of toxicity to living cells.'),
(4202, NULL, 'Unintended Presence of Allergens', NULL, 'Unintended or unexpected presence of allergens in the device. If the presence of the allergen is expected but not adequately labelled, then use \"Labelling Problem\".'),
(4203, NULL, 'Electrical/Electronic Component Problem Identified', NULL, 'The performance of an electrical or electronic component was found to be inadequate.'),
(4204, NULL, 'Unintended Emission', NULL, 'Problems due to unintended emission of electromagnetic energy by the device.'),
(4205, NULL, NULL, 'Network Communication Problem', 'Communications problems between devices within a network system.'),
(4206, NULL, 'Device Not Compatible With Another Device', NULL, 'A device that malfunctions due to being used in combination with, or in the presence of, another device.'),
(4207, NULL, 'Unintended Compatibility', NULL, 'The device was confirmed to be compatible with another device with which the device is intended to be incompatible.'),
(4208, NULL, 'Inadequate or Incorrect Instructions for Maintenance', NULL, 'Inadequate or incorrect information in the instructions for maintenance.'),
(4209, NULL, 'Inadequate Physicochemical Properties', NULL, 'Problems that occur due to the physicochemical properties.'),
(4210, NULL, 'Leakage/Seal', NULL, 'Problems caused by inadequate/broken seal within the device.'),
(4211, NULL, 'Incorrect Dimension', NULL, 'Problems caused by incorrect physical dimensions of the device or one of its parts'),
(4212, NULL, 'Light Source Problem Identified', NULL, 'Problems with the optical properties of a device such as diopter, glare, and irradiance or glistening.'),
(4213, NULL, 'Software Maintenance Problem Identified', NULL, 'The device software was not maintained/updated properly.'),
(4214, NULL, 'Erroneous Data Transfer', NULL, 'The device software fails to transfer the expected data within a system or to another device.'),
(4215, NULL, 'Data Storage or Loss of Data', NULL, 'Storage of data was unsuccessful in total or in part.'),
(4216, NULL, 'Overheating Problem Identified', NULL, 'The device was found to become hotter than expected during operation. This applies to devices which are not intended to deliver heat. Use \"Excessive heating identified\" for devices which are intended to deliver heat during operation. Use \"Inadequate cooling identified\" if the overheating was related to a problem with a cooling system.'),
(4217, NULL, 'Excessive Heating Identified', NULL, 'The device delivered more heat than intended or expected during operation. This applies to devices which are intended to deliver heat. Use \"Overheating problem identified\" for devices which are not intended to deliver heat during operation.'),
(4218, NULL, 'Excessive Cooling Identified', NULL, 'The device cooled the patient or another device more than intended or expected during operation.'),
(4219, NULL, 'Inadequate Cooling Identified', NULL, 'The device did not sufficiently cool the patient or another device during operation.'),
(4220, NULL, 'Fail-safe Problem Identified', NULL, 'A system intended to prevent unsafe operation of the device did not operate correctly.'),
(4221, NULL, 'Alarm System Problem Identified', NULL, 'A system intended to warn of a potentially unsafe condition did not operate correctly.'),
(4222, NULL, 'Problem of Device to Self-Test', NULL, 'Malfunction of the device\'s self-test system.'),
(4223, NULL, 'Problem to Auto Stop', NULL, 'An auto stop function of a device did not operate correctly.'),
(4224, NULL, 'Premature Indicator Activation', NULL, 'A system intended to indicate the device status was triggered prematurely.'),
(4225, NULL, 'Reset Problem', NULL, 'The device does not reset properly.'),
(4226, NULL, 'Shielding Problem', NULL, 'Inadequate shielding of/by the device.'),
(4227, NULL, 'Missing or Inadequate Safety Measures', NULL, 'Safety measures are inadequately applied or missing.'),
(4228, NULL, 'Device Incorrectly Reprocessed', NULL, 'Problems associated with the failure to properly and adequately reprocess the device.'),
(4229, NULL, NULL, 'Device Incorrectly Cleaned During Reprocessing', 'The cleaning procedure is not followed correctly or used inappropriate cleaning materials.'),
(4230, NULL, NULL, 'Device Incorrectly Disinfected/Sterilised During Reprocessing', 'The disinfection/sterilization process was incorrect and/or the wrong products for disinfection/sterilization were used.'),
(4231, NULL, NULL, 'Device Incorrectly Assembled During Reprocessing', 'Incorrect assembly of the device following reprocessing.'),
(4232, NULL, 'Incorrect Interpretation of Results/Data', NULL, 'Problems resulting from the incorrect interpretation by the user of the results or data provided by the device.'),
(4233, 'Patient Sample Problem', NULL, NULL, 'Problems that occurred due to endogenous or exogenous interferent in the sample, or unexpected variation in the target analyte/marker.'),
(4234, NULL, 'New or Unknown Interferent', NULL, 'New or unknown endogenous or exogenous interferent (sample) identified.'),
(4235, NULL, 'Known Interferent', NULL, 'Known interferent in the sample identified.'),
(4236, NULL, 'Change in Target Marker/Variant/ Mutant', NULL, 'Problem due to change in target marker/variant/mutant which is not covered in the labelling.'),
(4237, NULL, 'Pre-analytical Handling Problem', NULL, 'Incorrect pre-analytical handling of patient\'s sample by the user.'),
(4238, NULL, 'Contamination of Environment by Device', NULL, 'Operation of the device results in contamination of the nearby environment e.g. dust, dirt, smoke, heat or biological material.'),
(4239, NULL, 'Environmental Pressure Problem Identified', NULL, 'Device performance was affected by the pressure, or changes in pressure, of the environment in which it was used.'),
(4240, NULL, 'Ambient Light Problem Identified', NULL, 'Device performance was affected by ambient light. This term applies to the direct effects of ambient light on the device, and to the user\'s ability to operate the device (e.g. to read device output).'),
(4241, NULL, 'Sterilization Problem Identified', NULL, 'Problems that occurred during terminal sterilization by the manufacturer.'),
(4242, NULL, 'Maintenance of Manufacturing Machinery', NULL, 'Problems caused by failure to maintain manufacturing equipment used to produce the device.'),
(4243, NULL, NULL, 'Packaging Materials Problem', 'Problems that occurred because of the composition or type of packaging materials was inappropriate for the device.'),
(4244, NULL, NULL, 'Packaging Contains Unintended Material', 'Problems that occurred because unintended material was packaged with the device.'),
(4245, NULL, NULL, 'Packaging Contains Incorrect or Incomplete Device', 'Problems that occurred because the packaging contained an incorrect or incomplete device (missing components).'),
(4246, 'Transport/Storage Problem Identified', NULL, NULL, 'Problems was caused by transport or storage conditions.'),
(4247, 'Appropriate Term/Code Not Available', NULL, NULL, 'Problems is not adequately described by any other term. Note: This code must not be used unless there is no other feasible code. The preferred term should be documented when submitting an adverse event report. This information will be used to determine if a new term should be added to the code table.'),
(4248, 'Usage Problem Identified', NULL, NULL, 'Problems that occurred related to the actions of a healthcare professional, patient, or other device user.'),
(4249, NULL, 'Artificial Intelligence Training/Validation Problem Identified  ', NULL, 'Problem associated with the training and/or validation of artificial intelligence, including machine learning algorithms.'),
(4250, NULL, 'Corrupt Software', NULL, 'The device software becomes corrupted and results in device malfunction. '),
(4251, NULL, 'Undesirable Presence of Endogenous Materials', NULL, 'Undesirable presence of endogenous substances, body fluids, cellular tissues, etc.'),
(4252, NULL, 'Corrupted memory', NULL, 'Malfunction that resulted from a device memory corruption, including bit flips or single event errors.'),
(4253, NULL, 'Blockage Identified', NULL, 'Problems that occurred due to an obstruction or blockage.'),
(4254, NULL, 'Insufficient Sample Volume', NULL, 'Not having a sufficient volume of sample to perform a test.'),
(4255, NULL, 'Use of Non-Validated Controls Identified', NULL, 'Problems that occur related to the use of non-validated controls.'),
(4256, 'Malfunction Observed Without Conclusive Finding', NULL, NULL, 'Malfunction was verified but no conclusive finding is available.'),
(4257, NULL, 'Misadjustment/misalignment identified', NULL, 'Problems caused by incorrect adjustment of device components.');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `event_ticket_response`
--
ALTER TABLE `event_ticket_response`
  ADD PRIMARY KEY (`response_cd`);

--
-- Indices de la tabla `fda_annex_c`
--
ALTER TABLE `fda_annex_c`
  ADD PRIMARY KEY (`fda_cd`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `event_ticket_response`
--
ALTER TABLE `event_ticket_response`
  MODIFY `response_cd` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
