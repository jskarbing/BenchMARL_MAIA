### Changes made in order to add our custom Melting Pot MAIA environment:
- Renamed folder benchmarl/environments/meltingpot to meltingpot_maia, and made the following changes within:
    - Modified MeltingpotTask in the existing common.py file to add HARVEST_MAIA to the task list (and import the updated wrapper; see below)
    - Added a modified torchrl_meltingpot_wrapper.py file for adjusting MeltingpotEnv and MeltingpotWrapper (originally from TorchRL) to work with our custom envs
    - Added a meltingpot_lib folder for all modified Meltingpot library files
        - Added a config/substrates/__init__.py file for adding to SUBSTRATES, and updating get_config
        - Added a config/substrates/harvest__maia.py file for our custom env
        - Added a substrate.py file for adjusting Substrate
        - Added a human_play/play_commons_harvest.py file modifying the original play_commons_harvest.py file from dm-meltingpot,
        for human play for our custom envs (and as a way to test that it works as expected)
- Added a harvest__maia.yaml file for our custom env to benchmarl/conf/task/meltingpot
- Added cnn architecture cnn_maia (as a yaml file) to BenchMARL/benchmarl/conf/model/layers.

### Other changes
- Replaced project_name with wandb_kwargs in experiment configs, and made the corresponding changes in experiment.py and logger.py, to allow for specifying other wandb kwargs than only the project name.