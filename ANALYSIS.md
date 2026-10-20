## How well did you reproduce the original results? What differed?

The results were reproducible fairly easily and it was more or less similar to the original result. We added the non linear framework alongwith the paper's simulation to understand the situation
more closely, i.e. how actually the logistic performs in various scenarios.

## Were there any design choices that favored certain methods?

Not really! Both the methods were far from logistic model, hence there was a strong bias in the $beta_2$ for both the models.

## Were realistic scenarios included, or only idealixed conditions?

Actually the paper tries to show scenarios when the logistic model is not followed, so I would say it depends on the allocation. In real life, generally data is from observational study, so
it is difficult to say which model it came from, since there will always be confounders.

## What would you change about the simulation design? Why?

It might be helful to add more designs to see how it performs in various type of misspecification.

## Did you recreate the visualizations or make your own? What did the visualizations reveal that the original paper missed or undersold?

There was no visualization in the original paper. So, it is difficult to understand how things are going in various dimensions. I made my own plots which I believe is 
much more informative than the tables. 

## What was surprising or unexpected in the results?

I didn't expect such a strict bias, but is mathematically evident by Jensen's inequality. 
