DROP TABLE IF EXISTS test_results;
DROP TABLE IF EXISTS devices;

CREATE TABLE [devices] (
  [id] int PRIMARY KEY IDENTITY(1, 1),
  [name] nvarchar(255) NOT NULL,
  [description] nvarchar(255),
  [software_version] nvarchar(255),
)


CREATE TABLE [test_results] (
  [id] int PRIMARY KEY IDENTITY(1, 1),
  [sc1] bit,
  [sc2] bit,
  [bdb1] bit,
  [bdb2] bit,
  [bdb3] bit,
  [amsdu1] bit,
  [amsdu2] bit,
  [amsdu3] bit,
  [mk1] bit,
  [mk2] bit,
  [ca1] bit,
  [ca2] bit,
  [ca3] bit,
  [ca4] bit,
  [ncpn1] bit,
  [mpe1] bit,
  [mpe2] bit,
  [mpe3] bit,
  [mpe4] bit,
  [mpe5] bit,
  [bfa1] bit,
  [bfa2] bit,
  [eapol1] bit,
  [eapol2] bit,
  [eapol3] bit,
  [eapol4] bit,
  [device1_id] int,
  [device2_id] int
)


ALTER TABLE [test_results] ADD FOREIGN KEY ([device1_id]) REFERENCES [devices] ([id])


ALTER TABLE [test_results] ADD FOREIGN KEY ([device2_id]) REFERENCES [devices] ([id])



